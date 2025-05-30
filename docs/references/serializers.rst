.. _references_serializers:

===========
Serializers
===========

These are the
`DRF serializers <https://www.django-rest-framework.org/api-guide/serializers/>`_ used
in :ref:`references_viewsets` to serialize data from database to output format like XML
or JSON.

Serializers are also able to deserialize content from XML or JSON inputs.

.. automodule:: djangoapp_sample.serializers.article
    :members: ArticleSerializer, ArticleResumeSerializer

.. automodule:: djangoapp_sample.serializers.blog
    :members: BlogSerializer, BlogResumeSerializer
