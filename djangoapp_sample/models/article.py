from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .blog import Blog


class Article(models.Model):
    """
    A simple article for a blog.

    Attributes:
        blog (models.ForeignKey): Required related Blog object.
        title (models.CharField): Required title string.
        content (models.TextField): Optionnal text content.
        publish_start (models.DateTimeField): Required publication date determine
            when article will be available.
    """
    blog = models.ForeignKey(
        Blog,
        verbose_name="Related blog",
        on_delete=models.CASCADE
    )

    title = models.CharField(
        _("title"),
        blank=False,
        max_length=150,
        default="",
    )

    content = models.TextField(
        _("content"),
        blank=True,
        default="",
    )

    publish_start = models.DateTimeField(
        _("publication start"),
        db_index=True,
        default=timezone.now,
    )

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = [
            "-publish_start",
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Return absolute URL to the article detail view.

        Returns:
            string: An URL.
        """
        return reverse("djangoapp_sample:article-detail", args=[
            str(self.blog.id),
            str(self.id)
        ])
