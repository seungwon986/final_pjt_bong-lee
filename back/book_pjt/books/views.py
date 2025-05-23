from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer, CategorySerializer
from .utils import import_books_from_aladin
from datetime import datetime
from .models import Book, Category
from .utils import process_book_vectors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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

@api_view(['POST'])
def generate_book_vectors(request):
    process_book_vectors()
    return Response({"message": "도서 벡터 생성 완료"}, status=200)

@api_view(['POST'])
def recommend_books(request):
    preferred_ids = request.data.get('preferred_books', [])
    if not preferred_ids:
        return Response({'error': 'preferred_books 값이 필요합니다.'}, status=400)

    books = Book.objects.exclude(vector__isnull=True)
    book_map = {book.id: book for book in books}

    # 선택된 벡터 가져오기
    vectors = []
    for book_id in preferred_ids:
        book = book_map.get(book_id)
        if book and book.vector:
            vectors.append(book.vector)
    if not vectors:
        return Response({'error': '유효한 벡터를 가진 preferred_books 없음'}, status=400)

    mean_vector = np.mean(vectors, axis=0).reshape(1, -1)

    # 모든 도서와의 유사도 계산
    similarity_list = []
    for book in books:
        if book.id in preferred_ids:
            continue
        if book.vector:
            sim = cosine_similarity([mean_vector[0]], [book.vector])[0][0]
            similarity_list.append((sim, book))

    # 유사도 상위 10개 도서 추천
    similarity_list.sort(reverse=True, key=lambda x: x[0])
    top_books = [book for _, book in similarity_list[:10]]

    serializer = BookSerializer(top_books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': '해당 도서를 찾을 수 없습니다.'}, status=404)

    serializer = BookSerializer(book)
    return Response(serializer.data)