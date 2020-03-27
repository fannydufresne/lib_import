from django.db import models


class BaseModel(models.Model):
    """Defines a model to be used as foreign key."""

    name = models.CharField(
        max_length=256,
    )


class ExampleModel(models.Model):
    """Defines an example model."""

    date = models.DateTimeField(
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=256,
    )
    base = models.ForeignKey(
        BaseModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
