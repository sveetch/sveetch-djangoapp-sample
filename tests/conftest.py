"""
Pytest fixtures
"""
from pathlib import Path

import pytest

import djangoapp_sample
from djangoapp_sample.factories.cms import PageFactory


class FixturesSettingsTestMixin(object):
    """
    A mixin containing settings about application. This is almost about useful
    paths which may be used in tests.

    Attributes:
        application_path (pathlib.Path): Absolute path to the application directory.
        application_urlpath (pathlib.Path): URL path to the application as mounted
            in project ``urls.py``.
        package_path (pathlib.Path): Absolute path to the package directory.
        tests_dir (pathlib.Path): Directory name which include tests.
        tests_path (pathlib.Path): Absolute path to the tests directory.
        fixtures_dir (pathlib.Path): Directory name which include tests datas.
        fixtures_path (pathlib.Path): Absolute path to the tests datas.
    """
    def __init__(self):
        self.application_path = Path(
            djangoapp_sample.__file__
        ).parents[0].resolve()
        self.application_urlpath = "djangoapp_sample"

        self.package_path = self.application_path.parent

        self.tests_dir = "tests"
        self.tests_path = self.package_path / self.tests_dir

        self.fixtures_dir = "data_fixtures"
        self.fixtures_path = self.tests_path / self.fixtures_dir

    def format(self, content):
        """
        Format given string to include some values related to this application.

        Arguments:
            content (str): Content string to format with possible values.

        Returns:
            str: Given string formatted with possible values.
        """
        return content.format(
            HOMEDIR=Path.home(),
            PACKAGE=str(self.package_path),
            APPLICATION=str(self.application_path),
            URLPATH=str(self.application_urlpath),
            TESTS=str(self.tests_path),
            FIXTURES=str(self.fixtures_path),
            VERSION=djangoapp_sample.__version__,
        )


@pytest.fixture(scope="function")
def temp_builds_dir(tmp_path):
    """
    Prepare a temporary build directory.

    NOTE: You should use directly the "tmp_path" fixture in your tests.
    """
    return tmp_path


@pytest.fixture(scope="module")
def tests_settings():
    """
    Initialize and return settings for tests.

    Example:
        You may use it in tests like this: ::

            def test_foo(tests_settings):
                print(tests_settings.package_path)
                print(tests_settings.format("Application version: {VERSION}"))
    """
    return FixturesSettingsTestMixin()


@pytest.fixture(scope="function")
def cms_homepage(db, settings):
    """
    Create a random CMS homepage.

    At least a homepage is required for test using views else CMS will make fails
    view url resolving since of its middleware.
    """
    page = PageFactory(**{
        "title__title": "Homepage",
        "parent": None,
        "reverse_id": "homepage",
        "set_homepage": True,
        "should_publish": True,
        "in_navigation": True,
        "title__language": settings.LANGUAGE_CODE,
        "title__slug": "homepage",
        "template": settings.TEST_PAGE_TEMPLATES,
    })
    return page
