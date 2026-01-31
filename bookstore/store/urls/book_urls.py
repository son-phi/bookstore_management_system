from django.urls import path
from store.controllers.bookController.book_controller import list_books, book_detail

urlpatterns = [
    path("books/", list_books),
    path("books/<int:book_id>/", book_detail),
]
