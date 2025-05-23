from django.db import models
from django.db.models import JSONField 

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    pub_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=50, unique=True)
    cover = models.URLField(blank=True)
    description = models.TextField(blank=True)
    customer_review_rank = models.PositiveIntegerField(default=0)
    vector = models.JSONField(null=True, blank=True)


    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
