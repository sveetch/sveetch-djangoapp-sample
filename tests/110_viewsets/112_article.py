import datetime

import pytest

from rest_framework.test import APIClient

from djangoapp_sample.compat.import_zoneinfo import ZoneInfo
from djangoapp_sample.factories import (
    ArticleFactory, BlogFactory, UserFactory
)
from djangoapp_sample.models import Article

from djangoapp_sample.utils.tests import DRF_DUMMY_HOST_URL as HOSTURL


def test_article_viewset_list(db, settings):
    """
    Read response from API viewset list.
    """
    default_tz = ZoneInfo(settings.TIME_ZONE)

    # Create some articles
    lorem = ArticleFactory(
        title="Lorem",
        content="Ipsume salace nec vergiture",
        publish_start=datetime.datetime(2012, 10, 15, 12, 00).replace(
            tzinfo=default_tz
        ),
    )
    bonorum = ArticleFactory(
        title="Bonorum",
        content="Sed ut perspiciatis unde",
        publish_start=datetime.datetime(2021, 8, 7, 15, 30).replace(
            tzinfo=default_tz
        ),
    )

    # Use test client to get article list
    client = APIClient()
    response = client.get("/djangoapp_sample/api/articles/", format="json")
    json_data = response.json()

    # Expected payload from JSON response
    expected = [
        {
            "id": bonorum.id,
            "url": "{}/djangoapp_sample/api/articles/{}/".format(
                HOSTURL,
                bonorum.id
            ),
            "view_url": "{}/djangoapp_sample/{}/{}/".format(
                HOSTURL,
                bonorum.blog_id,
                bonorum.id
            ),
            "blog": {
                "id": bonorum.blog_id,
                "url": "{}/djangoapp_sample/api/blogs/{}/".format(
                    HOSTURL,
                    bonorum.blog_id
                ),
                "view_url": "{}/djangoapp_sample/{}/".format(
                    HOSTURL,
                    bonorum.blog_id
                ),
                "title": bonorum.blog.title,
            },
            "publish_start": bonorum.publish_start.isoformat(),
            "title": bonorum.title,
        },
        {
            "id": lorem.id,
            "url": "{}/djangoapp_sample/api/articles/{}/".format(
                HOSTURL,
                lorem.id
            ),
            "view_url": "{}/djangoapp_sample/{}/{}/".format(
                HOSTURL,
                lorem.blog_id,
                lorem.id
            ),
            "blog": {
                "id": lorem.blog_id,
                "url": "{}/djangoapp_sample/api/blogs/{}/".format(
                    HOSTURL,
                    lorem.blog_id
                ),
                "view_url": "{}/djangoapp_sample/{}/".format(
                    HOSTURL,
                    lorem.blog_id
                ),
                "title": lorem.blog.title,
            },
            "publish_start": lorem.publish_start.isoformat(),
            "title": lorem.title,
        },
    ]

    assert response.status_code == 200
    assert expected == json_data


def test_article_viewset_detail(db, settings):
    """
    Read response from API viewset detail.
    """
    default_tz = ZoneInfo(settings.TIME_ZONE)

    # Create article object
    lorem = ArticleFactory(
        title="Lorem",
        content="Ipsume salace nec vergiture",
        publish_start=datetime.datetime(2012, 10, 15, 12, 00).replace(
            tzinfo=default_tz
        ),
    )

    # Use test client to get article object
    client = APIClient()
    response = client.get(
        "/djangoapp_sample/api/articles/{}/".format(lorem.id),
        format="json"
    )
    json_data = response.json()

    # Expected payload from JSON response
    expected = {
        "id": lorem.id,
        "url": "{}/djangoapp_sample/api/articles/{}/".format(
            HOSTURL,
            lorem.id
        ),
        "view_url": "{}/djangoapp_sample/{}/{}/".format(
            HOSTURL,
            lorem.blog_id,
            lorem.id
        ),
        "blog": {
            "id": lorem.blog_id,
            "url": "{}/djangoapp_sample/api/blogs/{}/".format(
                HOSTURL,
                lorem.blog_id
            ),
            "view_url": "{}/djangoapp_sample/{}/".format(
                HOSTURL,
                lorem.blog_id
            ),
            "title": lorem.blog.title,
        },
        "publish_start": lorem.publish_start.isoformat(),
        "title": lorem.title,
        "content": lorem.content,
    }

    assert response.status_code == 200
    assert expected == json_data


def test_article_viewset_forbidden(db):
    """
    Write methods require to be authenticated with the right permissions.
    """
    # Use test client with anonymous user
    client = APIClient()

    # Create article object
    foo = ArticleFactory(title="Foo")

    # Try to create a new article
    response = client.post(
        "/djangoapp_sample/api/articles/",
        {
            "title": "Ping",
        },
        format="json"
    )
    assert response.status_code == 403

    # Try to edit an existing article
    response = client.post(
        "/djangoapp_sample/api/articles/{}/".format(foo.id),
        {
            "title": "Bar",
        },
        format="json"
    )
    assert response.status_code == 403

    # Try to delete an existing article
    response = client.delete(
        "/djangoapp_sample/api/articles/{}/".format(foo.id),
        format="json"
    )
    assert response.status_code == 403


def test_article_viewset_post(db):
    """
    Create a new article with HTTP POST method.
    """
    # Create a superuser to not bother with permissions
    user = UserFactory(flag_is_superuser=True)

    # Create blog object
    foo = BlogFactory(title="Foo")

    # Use test client with authenticated user to create a new article
    client = APIClient()
    client.force_authenticate(user=user)

    # This will fail because of missing required fields
    response = client.post("/djangoapp_sample/api/articles/", {}, format="json")
    assert response.status_code == 400
    assert response.json() == {
        "blog_id": ["This field is required."],
        "title": ["This field is required."],
    }

    # This will succeed because every required field are given
    payload = {
        "title": "Lorem",
        "blog_id": foo.id,
        "content": "Ping pong",
    }
    response = client.post("/djangoapp_sample/api/articles/", payload, format="json")
    json_data = response.json()

    # Check response status code according to HTTP method
    assert response.status_code == 201

    # Check created object
    article = Article.objects.get(pk=json_data["id"])
    assert payload["title"] == json_data["title"]
    assert payload["content"] == json_data["content"]
    assert payload["title"] == article.title
    assert payload["content"] == article.content


def test_article_viewset_put(db, settings):
    """
    Edit an existing article with HTTP PUT method.
    """
    default_tz = ZoneInfo(settings.TIME_ZONE)

    # Use a superuser to not bother with permissions
    user = UserFactory(flag_is_superuser=True)

    # Create article object
    lorem = ArticleFactory(
        title="Lorem",
        content="Ipsume salace nec vergiture",
        publish_start=datetime.datetime(2012, 10, 15, 12, 00).replace(
            tzinfo=default_tz
        ),
    )

    # Use test client with authenticated user to create a new article
    payload = {
        "title": "Bar",
        "content": "Ping pong",
        "blog_id": lorem.blog_id,
    }
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.put(
        "/djangoapp_sample/api/articles/{}/".format(lorem.id),
        payload,
        format="json"
    )
    json_data = response.json()

    # Check response status code according to HTTP method
    assert response.status_code == 200

    # Check edited object
    article = Article.objects.get(pk=lorem.id)
    assert payload["title"] == json_data["title"]
    assert payload["content"] == json_data["content"]
    assert payload["title"] == article.title
    assert payload["content"] == article.content


def test_article_viewset_patch(db, settings):
    """
    Edit an existing article with HTTP PATCH method.
    """
    default_tz = ZoneInfo(settings.TIME_ZONE)

    # Use a superuser to not bother with permissions
    user = UserFactory(flag_is_superuser=True)

    # Create article object
    lorem = ArticleFactory(
        title="Lorem",
        content="Ipsume salace nec vergiture",
        publish_start=datetime.datetime(2012, 10, 15, 12, 00).replace(
            tzinfo=default_tz
        ),
    )

    # Use test client with authenticated user to create a new article
    payload = {
        "title": "Bar",
    }
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.patch(
        "/djangoapp_sample/api/articles/{}/".format(lorem.id),
        payload,
        format="json"
    )
    json_data = response.json()

    # Check response status code according to HTTP method
    assert response.status_code == 200

    # Check edited object
    article = Article.objects.get(pk=lorem.id)
    assert payload["title"] == json_data["title"]
    assert payload["title"] == article.title
    # content value has not been modified with patch, ensure it still original value
    assert json_data["content"] == article.content


def test_article_viewset_delete(db):
    """
    Edit an existing article with HTTP DELETE method.
    """
    # Create article object
    lorem = ArticleFactory()

    # Use a superuser to not bother with permissions
    user = UserFactory(flag_is_superuser=True)

    # Use test client with authenticated user to create a new article
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.delete("/djangoapp_sample/api/articles/{}/".format(lorem.id))

    # Check response status code according to HTTP method
    assert response.status_code == 204

    # Check deleted object does not exist anymore
    with pytest.raises(Article.DoesNotExist):
        Article.objects.get(pk=lorem.id)
