from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from store.models import Wishlist, WishlistItem, Book
from .auth_helpers import customer_login_required

@customer_login_required
def wishlist_view(request):
    user = request.current_user
    wishlist = Wishlist.objects.filter(userID=user).first()
    items = []
    if wishlist:
        items = WishlistItem.objects.filter(wishlistID=wishlist).select_related("bookID")
    return render(request, "customer/wishlist.html", {"wishlist": wishlist, "items": items})

@customer_login_required
def wishlist_add(request, book_id: int):
    if request.method != "POST":
        return redirect("/books/")

    user = request.current_user
    wishlist = Wishlist.objects.filter(userID=user).first()
    if not wishlist:
        wishlist = Wishlist.objects.create(userID=user, name="My Wishlist")

    book = get_object_or_404(Book, bookID=book_id)
    if not WishlistItem.objects.filter(wishlistID=wishlist, bookID=book).exists():
        WishlistItem.objects.create(wishlistID=wishlist, bookID=book, createdAt=timezone.now())

    return redirect("/wishlist/")

@customer_login_required
def wishlist_remove(request, item_id: int):
    if request.method != "POST":
        return redirect("/wishlist/")

    user = request.current_user
    wishlist = Wishlist.objects.filter(userID=user).first()
    if not wishlist:
        return redirect("/wishlist/")

    item = get_object_or_404(WishlistItem, itemID=item_id, wishlistID=wishlist)
    item.delete()
    return redirect("/wishlist/")
