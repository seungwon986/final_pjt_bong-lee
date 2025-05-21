from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    pub_date = models.DateField()
    isbn = models.CharField(max_length=20, unique=True)
    cover = models.URLField()
    publisher = models.CharField(max_length=100)
    customer_review_rank = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
