from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from store.models import Book, Category
from .staff_auth import staff_login_required
from decimal import Decimal

@staff_login_required
def book_list(request):
    query = request.GET.get("q", "").strip()
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(isbn__icontains=query)
        ).order_by("-bookID")
    else:
        books = Book.objects.all().order_by("-bookID")
    
    return render(request, "staff/books.html", {"books": books, "query": query})

@staff_login_required
def book_create(request):
    if request.method == "GET":
        categories = Category.objects.all().order_by("name")
        return render(request, "staff/book_form.html", {"categories": categories})

    title = request.POST.get("title", "").strip()
    isbn = request.POST.get("isbn", "").strip()
    price_raw = request.POST.get("price", "0").strip()
    stock_raw = request.POST.get("stock", "0").strip()
    desc = request.POST.get("description", "").strip()
    cat_id = request.POST.get("category_id", "").strip()

    try:
        price = Decimal(price_raw)
    except:
        price = Decimal("0.00")
    
    try:
        stock = int(stock_raw)
    except:
        stock = 0

    try:
        stock = int(stock_raw)
    except:
        stock = 0

    if not title or not isbn:
        categories = Category.objects.all().order_by("name")
        return render(request, "staff/book_form.html", {
            "categories": categories, 
            "error": "Title and ISBN required",
            "book": {"title": title, "isbn": isbn, "price": price, "stock": stock, "description": desc}
        })

    Book.objects.create(
        title=title,
        isbn=isbn,
        price=price,
        stock=stock,
        description=desc,
        categoryID_id=cat_id if cat_id else None
    )
    return redirect("/staff/books/")

@staff_login_required
def book_update(request, book_id):
    book = get_object_or_404(Book, bookID=book_id)
    if request.method == "GET":
        categories = Category.objects.all().order_by("name")
        return render(request, "staff/book_form.html", {"book": book, "categories": categories})

    title = request.POST.get("title", "").strip()
    isbn = request.POST.get("isbn", "").strip()
    price_raw = request.POST.get("price", "0").strip()
    # stock = request.POST.get("stock", "0").strip() # Stock usually managed via import slips, but allow edit here? 
    # User asked for "Update information (price, description)". 
    # Usually stock shouldn't be edited directly if we have proper inventory, but for simple edit let's allow description/price.
    desc = request.POST.get("description", "").strip()
    cat_id = request.POST.get("category_id", "").strip()

    try:
        price = Decimal(price_raw)
    except:
        price = Decimal("0.00")

    if not title or not isbn:
         categories = Category.objects.all().order_by("name")
         return render(request, "staff/book_form.html", {
            "categories": categories, 
            "error": "Title and ISBN required",
            "book": book
        })

    book.title = title
    book.isbn = isbn
    book.price = price
    book.description = desc
    if cat_id:
        book.categoryID_id = cat_id
    else:
        book.categoryID = None
    
    book.save()
    return redirect("/staff/books/")

@staff_login_required
def book_delete(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, bookID=book_id)
        book.delete()
    return redirect("/staff/books/")
