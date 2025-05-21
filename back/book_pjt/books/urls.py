from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list),
    path('import/', views.import_books_from_aladin),
]