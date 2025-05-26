import requests
from datetime import datetime
from .models import Book, Category
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

API_URL = 'http://www.aladin.co.kr/ttb/api/ItemList.aspx'
API_KEY = 'ttbtmddnjs36641349002'

CATEGORY_KEYWORDS = {
    "문학": ["소설", "시", "희곡"],
    "인문": ["인문학", "교양", "철학"],
    "사회과학": ["정치", "사회", "행정", "외교"],
    "과학": ["과학", "공학", "수학"],
    "자기계발": ["자기계발", "성공", "CEO", "리더"],
    "에세이": ["에세이", "수필"],
    "만화": ["만화", "웹툰"],
    "예술": ["예술", "영화", "음악", "디자인"],
    "경제/경영": ["경제", "경영", "비즈니스"],
    "종교/역사": ["종교", "역사"],
}

def normalize_category(category_name):
    for main_category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in category_name:
                return main_category
    return "기타"

def fetch_bestsellers_from_aladin(total_count=200):
    all_items = []
    per_page = 50
    pages = (total_count + per_page - 1) // per_page

    for page in range(pages):
        start = page
        params = {
            'TTBKey': API_KEY,
            'QueryType': 'Bestseller',
            'MaxResults': per_page,
            'Start': start,
            'SearchTarget': 'Book',
            'Output': 'js',
            'Version': 20131101,
            'CategoryId': '0',
            'Cover': 'Big',
        }

        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            try:
                items = response.json().get('item', [])
                all_items.extend(items)
            except Exception as e:
                print(f"[ERROR] JSON decode error on page {page + 1}: {e}")
        else:
            print(f"[ERROR] Page {page + 1} failed: {response.status_code}")

    return all_items

def import_books_from_aladin():
    items = fetch_bestsellers_from_aladin()
    imported = []

    for item in items:
        isbn = item.get('isbn')
        if not isbn:
            continue

        raw_category = item.get('categoryName', '')
        normalized = normalize_category(raw_category)
        category_obj, _ = Category.objects.get_or_create(name=normalized)

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
                    'category': category_obj,
                }
            )
            if created:
                imported.append(book)
        except Exception as e:
            print(f"[ERROR] 책 저장 실패 (ISBN: {isbn}): {e}")
            continue

    return imported

def process_book_vectors():
    books = Book.objects.filter(vector__isnull=True)
    if not books.exists():
        print("[INFO] 모든 책에 벡터가 이미 존재합니다.")
        return

    texts = []
    book_list = []

    for book in books:
        text = f"{book.title or ''} {book.author or ''} {book.category.name if book.category else ''} {book.description or ''}"
        texts.append(text)
        book_list.append(book)

    if not texts:
        print("[INFO] 벡터화할 텍스트가 없습니다.")
        return

    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(texts).toarray()

    for i, book in enumerate(book_list):
        book.vector = vectors[i].tolist()
        book.save()

    print(f"[INFO] {len(book_list)}권의 벡터가 새로 생성되었습니다.")
