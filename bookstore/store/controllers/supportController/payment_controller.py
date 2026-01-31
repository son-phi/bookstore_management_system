import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from store.models import Payment, PaymentMethod, Transaction, Order, OrderStatus, OrderHistory
from store.controllers.customerController.auth_helpers import customer_login_required
from django.db import transaction
from django.db.models import F
from store.models import OrderDetail, Book, Shipment, ShippingTrace


def _ensure_status(name: str, description: str) -> OrderStatus:
    status, _ = OrderStatus.objects.get_or_create(
        name=name,
        defaults={"description": description},
    )
    return status


@customer_login_required
def payment_methods(request):
    # list methods for UI/debug
    methods = PaymentMethod.objects.filter(isActive=True).order_by("name")
    return render(request, "support/payment_methods.html", {"methods": methods})


@customer_login_required
def payment_create_for_order(request, order_id: int):
    """
    Create payment for an order (called after checkout).
    method is passed via POST: 'COD' or 'ONLINE' (or method name).
    """
    if request.method != "POST":
        return redirect(f"/orders/{order_id}/")

    user = request.current_user
    order = get_object_or_404(Order, orderID=order_id)

    # ownership check
    if order.userID_id != user.userID:
        return redirect("/books/")

    method = request.POST.get("method", "COD").strip().upper()
    amount = order.totalAmount  # Decimal field already

    # create or replace existing payment for the order (simple approach)
    payment = Payment.objects.filter(orderID=order).first()
    if not payment:
        payment = Payment.objects.create(
            orderID=order,
            amount=amount,
            status="PENDING" if method == "ONLINE" else "COD",
            method=method,
        )
    else:
        payment.amount = amount
        payment.method = method
        payment.status = "PENDING" if method == "ONLINE" else "COD"
        payment.save(update_fields=["amount", "method", "status"])

    # If COD: mark order as PLACED (already), go order detail
    if method != "ONLINE":
        placed = _ensure_status("PLACED", "Order placed")
        OrderHistory.objects.create(
            orderID=order,
            statusID=placed,
            changedBy=user,
            changedAt=timezone.now(),
        )
        return redirect(f"/orders/{order.orderID}/")

    # ONLINE: go to payment page
    return redirect(f"/payments/{payment.paymentID}/")


@customer_login_required
def payment_detail(request, payment_id: int):
    user = request.current_user
    payment = get_object_or_404(Payment, paymentID=payment_id)
    order = payment.orderID

    # ownership check
    if order.userID_id != user.userID:
        return redirect("/books/")

    tx = Transaction.objects.filter(paymentID=payment).order_by("-timestamp").first()

    return render(
        request,
        "support/payment_detail.html",
        {"payment": payment, "order": order, "transaction": tx},
    )


@customer_login_required
def payment_confirm(request, payment_id: int):
    """
    Mock gateway confirm (IPN-like).
    BUSINESS:
    - If success:
        1) Mark Payment SUCCESS
        2) Create Transaction
        3) Deduct Book.stock by OrderDetail.quantity (fail if insufficient)
        4) OrderHistory -> PAID
        5) Create Shipment + ShippingTrace (CREATED)
    """
    if request.method != "POST":
        return redirect(f"/payments/{payment_id}/")

    user = request.current_user

    with transaction.atomic():
        payment = get_object_or_404(Payment.objects.select_for_update(), paymentID=payment_id)
        order = payment.orderID

        # ownership check
        if order.userID_id != user.userID:
            return redirect("/books/")

        # only confirm when pending online
        if payment.method != "ONLINE":
            return redirect(f"/payments/{payment_id}/")

        if payment.status == "SUCCESS":
            return redirect(f"/payments/{payment_id}/")

        # Load order details with lock for consistency
        details = list(
            OrderDetail.objects.select_related("bookID")
            .select_for_update()
            .filter(orderID=order)
        )

        # 1) Validate stock
        # lock books too (via select_for_update)
        book_ids = [d.bookID_id for d in details]
        books = {b.bookID: b for b in Book.objects.select_for_update().filter(bookID__in=book_ids)}

        for d in details:
            b = books.get(d.bookID_id)
            if b is None:
                return render(request, "support/payment_detail.html", {
                    "payment": payment, "order": order, "transaction": None,
                    "error": "Book not found for order item"
                })
            if b.stock < d.quantity:
                # insufficient stock -> do NOT confirm
                return render(request, "support/payment_detail.html", {
                    "payment": payment, "order": order, "transaction": None,
                    "error": f"Insufficient stock for '{b.title}'. Available={b.stock}, required={d.quantity}"
                })

        # 2) Deduct stock (use F for safe update)
        for d in details:
            Book.objects.filter(bookID=d.bookID_id).update(stock=F("stock") - d.quantity)

        # 3) Mark payment success
        payment.status = "SUCCESS"
        payment.save(update_fields=["status"])

        # 4) Create transaction log
        Transaction.objects.create(
            paymentID=payment,
            gatewayRef=f"MOCK-{uuid.uuid4().hex[:12].upper()}",
            timestamp=timezone.now(),
        )

        # 5) Update order history -> PAID
        paid = _ensure_status("PAID", "Payment success")
        OrderHistory.objects.create(
            orderID=order,
            statusID=paid,
            changedBy=user,
            changedAt=timezone.now()
        )

        # 6) Auto create shipment if not exists
        shipment = Shipment.objects.filter(orderID=order).first()
        if not shipment:
            shipment = Shipment.objects.create(
                orderID=order,
                trackingCode=f"TRK-{uuid.uuid4().hex[:10].upper()}",
                status="CREATED"
            )
            ShippingTrace.objects.create(
                shipmentID=shipment,
                location="WAREHOUSE",
                status="CREATED",
                time=timezone.now()
            )

    return redirect(f"/orders/{order.orderID}/")



@customer_login_required
def payment_refund(request, payment_id: int):
    """
    Mock refund: set status REFUNDED, add OrderHistory.
    """
    if request.method != "POST":
        return redirect(f"/payments/{payment_id}/")

    user = request.current_user
    payment = get_object_or_404(Payment, paymentID=payment_id)
    order = payment.orderID

    if order.userID_id != user.userID:
        return redirect("/books/")

    if payment.status == "REFUNDED":
        return redirect(f"/payments/{payment_id}/")

    payment.status = "REFUNDED"
    payment.save(update_fields=["status"])

    refunded = _ensure_status("REFUNDED", "Payment refunded")
    OrderHistory.objects.create(
        orderID=order,
        statusID=refunded,
        changedBy=user,
        changedAt=timezone.now(),
    )

    return redirect(f"/orders/{order.orderID}/")
