from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Category, Book

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    CATEGORY_CHOICES = [
        ('novel', '소설/시/희곡'),
        ('economy', '경제/경영'),
        ('science', '과학'),
        ('self', '자기계발'),
        ('human', '인문/교양'),
        ('kids', '어린이/청소년'),
    ]

    birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    nickname = models.CharField(max_length=20, unique=True)

    # ✅ 새로 추가된 다대다 필드
    preferred_categories = models.ManyToManyField(Category, blank=True)
    preferred_books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.username
