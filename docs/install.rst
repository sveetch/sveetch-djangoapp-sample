.. _install_intro:

=======
Install
=======

Install package in your environment : ::

    pip install sveetch-djangoapp-sample

For development usage see :ref:`development_install`.

Configuration
*************

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        "rest_framework",
        "djangoapp_sample",
    )

Then load default application settings in your settings file: ::

    from djangoapp_sample.settings import *

Then mount applications URLs: ::

    urlpatterns = [
        ...
        path("", include("djangoapp_sample.urls")),
    ]

And finally apply database migrations.

Settings
********

.. automodule:: djangoapp_sample.settings
   :members:
