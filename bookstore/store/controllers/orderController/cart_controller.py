from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from store.models import Book, Cart, CartItem, UserBehavior
from store.controllers.customerController.auth_helpers import get_current_user

def _get_or_create_cart(request) -> Cart:
    # ensure session
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    user = get_current_user(request)

    cart = Cart.objects.filter(sessionKey=session_key).first()
    if not cart:
        cart = Cart.objects.create(userID=user, sessionKey=session_key, updatedAt=timezone.now())
    else:
        # attach user if newly logged in
        if user and cart.userID is None:
            cart.userID = user
        cart.updatedAt = timezone.now()
        cart.save(update_fields=["userID", "updatedAt"])
    return cart

def cart_view(request):
    cart = _get_or_create_cart(request)
    items = CartItem.objects.filter(cartID=cart).select_related("bookID")
    total = 0
    for it in items:
        total += float(it.bookID.price) * it.quantity
    return render(request, "order/cart.html", {"cart": cart, "items": items, "total": total})

def cart_add(request, book_id: int):
    if request.method != "POST":
        return redirect("/books/")

    cart = _get_or_create_cart(request)
    book = get_object_or_404(Book, bookID=book_id)

    item = CartItem.objects.filter(cartID=cart, bookID=book).first()
    if item:
        item.quantity += 1
        item.save(update_fields=["quantity"])
    else:
        CartItem.objects.create(cartID=cart, bookID=book, quantity=1)

    cart.updatedAt = timezone.now()
    cart.save(update_fields=["updatedAt"])
    return redirect("/cart/")

def cart_inc(request, item_id: int):
    if request.method != "POST":
        return redirect("/cart/")

    cart = _get_or_create_cart(request)
    item = get_object_or_404(CartItem, itemID=item_id, cartID=cart)
    item.quantity += 1
    item.save(update_fields=["quantity"])
    return redirect("/cart/")

def cart_dec(request, item_id: int):
    if request.method != "POST":
        return redirect("/cart/")

    cart = _get_or_create_cart(request)
    item = get_object_or_404(CartItem, itemID=item_id, cartID=cart)
    item.quantity -= 1
    if item.quantity <= 0:
        item.delete()
    else:
        item.save(update_fields=["quantity"])
    return redirect("/cart/")

def cart_set_qty(request, item_id: int):
    if request.method != "POST":
        return redirect("/cart/")

    cart = _get_or_create_cart(request)
    item = get_object_or_404(CartItem, itemID=item_id, cartID=cart)
    try:
        qty = int(request.POST.get("quantity", "1"))
    except ValueError:
        qty = 1
    if qty <= 0:
        item.delete()
    else:
        item.quantity = qty
        item.save(update_fields=["quantity"])
    return redirect("/cart/")

def cart_remove(request, item_id: int):
    if request.method != "POST":
        return redirect("/cart/")

    cart = _get_or_create_cart(request)
    item = get_object_or_404(CartItem, itemID=item_id, cartID=cart)
    item.delete()
    return redirect("/cart/")
