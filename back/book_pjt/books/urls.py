from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list),
    path('import/', views.import_books_from_aladin_view),
    path('categories/', views.category_list),
    path('generate-vectors/', views.generate_book_vectors, name='generate_book_vectors'),
    path('recommend/', views.recommend_books, name='recommend_books'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('preferred/', views.preferred_books_list, name='preferred_books'),

]