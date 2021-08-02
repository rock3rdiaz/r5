import uuid

from django.db import models


class Book(models.Model):
    """
    A basic book model
    """
    identifier = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    title = models.TextField()
    subtitle = models.TextField(null=True)
    author = models.TextField()
    categories = models.TextField(null=True)
    publication_date = models.CharField(max_length=20)
    publisher = models.TextField(null=True)
    description = models.TextField(null=True)
    image = models.TextField(null=True)
    source = models.CharField(max_length=10)
    modified_date = models.DateField(auto_now=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_date',)
