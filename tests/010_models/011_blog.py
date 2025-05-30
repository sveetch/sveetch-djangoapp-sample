from django.core.exceptions import ValidationError

import pytest

from djangoapp_sample.models import Blog


def test_basic(db):
    """
    Basic model validation with required fields should not fail
    """
    blog = Blog(
        title="Foo",
    )
    blog.full_clean()
    blog.save()

    url = "/djangoapp_sample/{blog_pk}/".format(
        blog_pk=blog.id,
    )

    assert 1 == Blog.objects.filter(title="Foo").count()
    assert "Foo" == blog.title
    assert url == blog.get_absolute_url()


def test_required_fields(db):
    """
    Basic model validation with missing required files should fail
    """
    blog = Blog()

    with pytest.raises(ValidationError) as excinfo:
        blog.full_clean()

    assert excinfo.value.message_dict == {
        "title": ["This field cannot be blank."],
    }
