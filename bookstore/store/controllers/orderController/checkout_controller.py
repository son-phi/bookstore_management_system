from django.shortcuts import redirect, render
from django.utils import timezone
from store.models import CartItem, Order, OrderDetail, OrderStatus, OrderHistory, PaymentMethod, Payment, Shipment, ShippingTrace
from store.controllers.customerController.auth_helpers import customer_login_required
from .cart_controller import _get_or_create_cart

@customer_login_required
def checkout(request):
    user = request.current_user
    cart = _get_or_create_cart(request)
    items = CartItem.objects.filter(cartID=cart).select_related("bookID")

    if request.method == "GET":
        total = 0
        for it in items:
            total += float(it.bookID.price) * it.quantity
            methods = PaymentMethod.objects.filter(isActive=True).order_by("name")
        return render(request, "order/checkout.html", {"items": items, "total": total, "methods": methods})

    # POST -> create order
    note = request.POST.get("note", "")
    shipping_fee = 0  # you can change later
    total_amount = 0
    for it in items:
        total_amount += float(it.bookID.price) * it.quantity

    order = Order.objects.create(
        userID=user,
        totalAmount=total_amount,
        shippingFee=shipping_fee,
        note=note
    )

    for it in items:
        OrderDetail.objects.create(
            orderID=order,
            bookID=it.bookID,
            price=it.bookID.price,
            quantity=it.quantity
        )

    # order history
    status, _ = OrderStatus.objects.get_or_create(name="PLACED", defaults={"description": "Order placed"})
    OrderHistory.objects.create(
        orderID=order,
        statusID=status,
        changedBy=user,
        changedAt=timezone.now()
    )

    # clear cart
    items.delete()

    method = request.POST.get("method", "COD").strip().upper()

    # create payment now (no need extra redirect)
    from store.models import Payment
    payment = Payment.objects.filter(orderID=order).first()
    if not payment:
        payment = Payment.objects.create(
            orderID=order,
            amount=order.totalAmount,
            status="PENDING" if method == "ONLINE" else "COD",
            method=method
        )
    else:
        payment.amount = order.totalAmount
        payment.method = method
        payment.status = "PENDING" if method == "ONLINE" else "COD"
        payment.save(update_fields=["amount", "method", "status"])

    if method == "ONLINE":
        return redirect(f"/payments/{payment.paymentID}/")
    return redirect(f"/orders/{order.orderID}/")



def order_detail(request, order_id: int):
    # simple order detail page without auth enforcement (demo)
    from django.shortcuts import get_object_or_404
    from store.models import Order, OrderDetail
    order = get_object_or_404(Order, orderID=order_id)
    details = OrderDetail.objects.filter(orderID=order).select_related("bookID")
    from store.models import Payment

    payment = Payment.objects.filter(orderID=order).first()
    shipment = Shipment.objects.filter(orderID=order).first()
    traces = []
    if shipment:
        traces = ShippingTrace.objects.filter(shipmentID=shipment).order_by("-time")

    return render(request, "order/order_detail.html", {"order": order, "details": details, "payment": payment, "shipment": shipment, "traces": traces})
