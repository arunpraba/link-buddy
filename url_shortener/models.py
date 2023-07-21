from django.db import models


from django.db import models


class ShortenedURL(models.Model):
    """Model definition for ShortenedURL."""

    id = models.AutoField(primary_key=True)
    original_url = models.URLField(unique=True)
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.short_code
