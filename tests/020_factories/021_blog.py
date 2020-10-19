from djangoapp_sample.factories import BlogFactory


def test_creation(db):
    """
    Factory should correctly create a new object without any errors
    """
    blog = BlogFactory(title="foo")
    assert blog.title == "foo"
