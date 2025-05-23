from rest_framework import serializers
from .models import Book, Category

# 카테고리 직렬화
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# 책 직렬화 (category를 CategorySerializer로 중첩)
class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # ⭐️ 요기!

    class Meta:
        model = Book
        fields = '__all__'
