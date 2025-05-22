from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer, CategorySerializer
from .utils import import_books_from_aladin
from datetime import datetime
from .models import Book, Category

@api_view(['GET'])
def book_list(request):
    category_ids = request.GET.getlist('category')
    book_ids = request.GET.getlist('id') 

    books = Book.objects.all()

    if category_ids:
        books = books.filter(category_id__in=category_ids)

    if book_ids:
        books = books.filter(id__in=book_ids)

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def import_books_from_aladin_view(request):
    if Book.objects.exists():
        return Response({'message': '이미 DB에 책이 있습니다. 가져오지 않음'}, status=200)

    imported = import_books_from_aladin()
    serializer = BookSerializer(imported, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)