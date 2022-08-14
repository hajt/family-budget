import uuid

from django.db import models


class CommonModel(models.Model):
    id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
