from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TimeStampedModel(models.Model):
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Snippet(TimeStampedModel):
    title = models.CharField(max_length=255)
    note = models.TextField()

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="snippets"
    )

    tags = models.ManyToManyField(Tag, related_name="snippets", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
