from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=CoverChoices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
