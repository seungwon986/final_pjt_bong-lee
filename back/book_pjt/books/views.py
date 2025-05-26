from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer, CategorySerializer
from .utils import import_books_from_aladin
from datetime import datetime
from .models import Book, Category
from .utils import process_book_vectors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json 

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
    import json  # ✅ 반드시 추가!

    preferred_ids = request.data.get('preferred_books', [])
    if not preferred_ids:
        return Response({'error': 'preferred_books 값이 필요합니다.'}, status=400)

    books = Book.objects.exclude(vector__isnull=True)
    book_map = {book.id: book for book in books}

    vectors = []
    for book_id in preferred_ids:
        book = book_map.get(book_id)
        if book and book.vector:
            try:
                raw_vector = book.vector if isinstance(book.vector, list) else json.loads(book.vector)
                vec = np.array(raw_vector).flatten()
                vectors.append(vec)
            except Exception as e:
                print(f"[ERROR] 벡터 파싱 실패 (book_id={book_id}): {e}")

    if not vectors:
        return Response({'error': '유효한 벡터를 가진 preferred_books 없음'}, status=400)

    mean_vector = np.mean(vectors, axis=0).reshape(1, -1)
    
    similarity_list = []
    for book in books:
        if book.id in preferred_ids:
            continue
        if book.vector:
            try:
                vector = np.array(book.vector if isinstance(book.vector, list) else json.loads(book.vector))
                sim = cosine_similarity(mean_vector, [vector])[0][0]
                similarity_list.append((sim, book))
            except Exception as e:
                print(f"[ERROR] 유사도 계산 실패 (book.id={book.id}): {e}")

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


@api_view(['POST'])
def preferred_books_list(request):
    preferred_ids = request.data.get('preferred_books', [])
    if not preferred_ids:
        return Response({'error': 'preferred_books 값이 필요합니다.'}, status=400)

    books = Book.objects.filter(id__in=preferred_ids)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)
