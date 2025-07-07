from django.db import models
from django.conf import settings

__all__ = ("Comment",)


class Comment(models.Model):
    product = models.ForeignKey(
        "products.Product",
        verbose_name="Product",
        on_delete=models.SET_NULL,
        related_name="comments",
        related_query_name="comment",
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Author",
        on_delete=models.SET_NULL,
        related_name="comments",
        related_query_name="comment",
        null=True,
        blank=True
    )
    masked_author_name = models.CharField(
        "Author's masked name",
        blank=True,
        null=True,
        max_length=255,
        editable=False
    )
    text = models.TextField(
        "Text",
        max_length=1000,
        null=True,
        blank=True
    )
    posted_at = models.DateTimeField(
        "Posted at",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ("-posted_at",)

    def save(self, *args, **kwargs):
        if self.author and not self.pk:
            self.masked_author_name = self.author.get_masked_fullname()
        return super().save(*args, **kwargs)

    def get_masked_author_name(self) -> str:
        return self.author.get_masked_fullname() if self.author else "Anonymous"