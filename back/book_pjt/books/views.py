from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .utils import fetch_bestsellers_from_aladin
from datetime import datetime

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def import_books_from_aladin(request):
    items = fetch_bestsellers_from_aladin()
    imported = []

    for item in items:
        isbn = item.get('isbn')
        if not isbn:
            continue

        try:
            book, created = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'title': item.get('title'),
                    'author': item.get('author'),
                    'pub_date': datetime.strptime(item.get('pubDate'), '%Y-%m-%d').date() if item.get('pubDate') else None,
                    'cover': item.get('cover'),
                    'publisher': item.get('publisher'),
                    'customer_review_rank': item.get('customerReviewRank', 0),
                    'description': item.get('description', '')[:1000],
                }
            )
            if created:
                imported.append(book)
        except Exception as e:
            print(f"[ERROR] ISBN {isbn}: {e}")
            continue

    serializer = BookSerializer(imported, many=True)
    return Response(serializer.data)
