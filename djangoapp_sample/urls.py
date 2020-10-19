"""
Application URLs
"""
from django.urls import path

from djangoapp_sample.views import (
    BlogIndexView, BlogDetailView,
    ArticleDetailView,
)


app_name = "djangoapp_sample"


urlpatterns = [
    path("", BlogIndexView.as_view(), name="blog-index"),
    path("<int:blog_pk>/", BlogDetailView.as_view(), name="blog-detail"),
    path(
        "<int:blog_pk>/<int:article_pk>/",
        ArticleDetailView.as_view(),
        name="article-detail"
    ),
]
