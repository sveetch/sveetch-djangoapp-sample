import datetime

from djangoapp_sample.compat.import_zoneinfo import ZoneInfo
from djangoapp_sample.factories import ArticleFactory, BlogFactory
from djangoapp_sample.serializers import ArticleSerializer


def test_article_serialize_single(db, settings):
    """
    Single object serialization.
    """
    default_tz = ZoneInfo(settings.TIME_ZONE)

    # Create blog
    foo = BlogFactory(title="Foo")

    # Create article
    lorem = ArticleFactory(
        blog=foo,
        title="Lorem",
        content="Ipsume salace nec vergiture",
        publish_start=datetime.datetime(2012, 10, 15, 12, 00).replace(
            tzinfo=default_tz
        ),
    )

    # Serialize article
    serializer = ArticleSerializer(lorem, context={"request": None})

    expected = {
        "id": lorem.id,
        "url": "/djangoapp_sample/api/articles/{}/".format(lorem.id),
        "view_url": "/djangoapp_sample/{}/{}/".format(foo.id, lorem.id),
        "blog": {
            "id": foo.id,
            "url": "/djangoapp_sample/api/blogs/{}/".format(foo.id),
            "view_url": "/djangoapp_sample/{}/".format(foo.id),
            "title": "Foo",
        },
        "title": "Lorem",
        "content": "Ipsume salace nec vergiture",
        "publish_start": "2012-10-15T12:00:00-05:00",
    }

    assert expected == serializer.data


def test_article_serialize_many(db, settings):
    """
    Many objects serialization.
    """
    default_tz = ZoneInfo(settings.TIME_ZONE)

    # Create some blogs
    foo = BlogFactory(title="Foo")
    bar = BlogFactory(title="Bar")

    # Create some articles
    lorem = ArticleFactory(
        blog=foo,
        title="Lorem",
        content="Ipsume salace nec vergiture",
        publish_start=datetime.datetime(2012, 10, 15, 12, 00).replace(
            tzinfo=default_tz
        ),
    )
    bonorum = ArticleFactory(
        blog=bar,
        title="Bonorum",
        content="Sed ut perspiciatis unde",
        publish_start=datetime.datetime(2021, 8, 7, 15, 30).replace(
            tzinfo=default_tz
        ),
    )

    # Serialize articles
    serializer = ArticleSerializer(
        [lorem, bonorum],
        many=True,
        context={"request": None}
    )

    expected = [
        {
            "id": lorem.id,
            "url": "/djangoapp_sample/api/articles/{}/".format(lorem.id),
            "view_url": "/djangoapp_sample/{}/{}/".format(foo.id, lorem.id),
            "blog": {
                "id": foo.id,
                "url": "/djangoapp_sample/api/blogs/{}/".format(foo.id),
                "view_url": "/djangoapp_sample/{}/".format(foo.id),
                "title": "Foo",
            },
            "title": "Lorem",
            "content": "Ipsume salace nec vergiture",
            "publish_start": "2012-10-15T12:00:00-05:00",
        },
        {
            "id": bonorum.id,
            "url": "/djangoapp_sample/api/articles/{}/".format(bonorum.id),
            "view_url": "/djangoapp_sample/{}/{}/".format(bar.id, bonorum.id),
            "blog": {
                "id": bar.id,
                "url": "/djangoapp_sample/api/blogs/{}/".format(bar.id),
                "view_url": "/djangoapp_sample/{}/".format(bar.id),
                "title": "Bar",
            },
            "title": "Bonorum",
            "content": "Sed ut perspiciatis unde",
            "publish_start": "2021-08-07T15:30:00-05:00",
        },
    ]

    assert expected == serializer.data
