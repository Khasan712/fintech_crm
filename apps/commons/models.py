from django.db import models


class CustomBaseAbstract(models.Model):
    creator = models.BigIntegerField(default=0)
    updater = models.BigIntegerField(default=0)
    deleter = models.BigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(blank=True, null=True, editable=False)
    deleted_at = models.DateTimeField(blank=True, null=True,  editable=False)

    class Meta:
        abstract = True


class CustomWeekAbstract(models.Model):
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    class Meta:
        abstract = True

