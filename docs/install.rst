.. _intro_install:

=======
Install
=======

Install package in your environment : ::

    pip install sveetch-djangoapp-sample

For development usage see :ref:`install_development`.

Configuration
*************

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        'djangoapp_sample',
    )

Then load default application settings in your settings file: ::

    from djangoapp_sample.settings import *

And finally apply database migrations.

Settings
********

.. automodule:: djangoapp_sample.settings
   :members:
