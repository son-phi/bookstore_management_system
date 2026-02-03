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
    from store.models import Carrier, ShippingRate

    if request.method == "GET":
        total_items_price = 0
        for it in items:
            total_items_price += float(it.bookID.price) * it.quantity
        
        methods = PaymentMethod.objects.filter(isActive=True).order_by("name")
        
        # Calculate shipping options
        # Assume "Inner City" for demo purposes, and weight 0.5 per item
        total_weight = sum([0.5 * it.quantity for it in items])
        carriers = Carrier.objects.all()
        carrier_options = []
        
        for c in carriers:
            # simple rate lookup
            rate = ShippingRate.objects.filter(carrierID=c, zone="Inner City", minWeight__lte=total_weight).order_by("-minWeight").first()
            fee = rate.price if rate else 30000
            carrier_options.append({
                "carrier": c,
                "fee": fee,
                "total_with_fee": total_items_price + float(fee)
            })

        return render(request, "order/checkout.html", {
            "items": items, 
            "total_items_price": total_items_price, 
            "methods": methods,
            "carrier_options": carrier_options
        })

    # POST -> create order
    note = request.POST.get("note", "")
    method = request.POST.get("method", "COD").strip().upper()
    carrier_id = request.POST.get("carrier", "")
    
    total_amount = 0
    for it in items:
        total_amount += float(it.bookID.price) * it.quantity

    # Calculate shipping fee again for security
    shipping_fee = 0
    selected_carrier = None
    if carrier_id:
        try:
            selected_carrier = Carrier.objects.get(carrierID=int(carrier_id))
            total_weight = sum([0.5 * it.quantity for it in items])
            rate = ShippingRate.objects.filter(carrierID=selected_carrier, zone="Inner City", minWeight__lte=total_weight).order_by("-minWeight").first()
            shipping_fee = float(rate.price) if rate else 30000.0
        except (ValueError, Carrier.DoesNotExist):
            pass

    final_total = total_amount + shipping_fee

    order = Order.objects.create(
        userID=user,
        totalAmount=final_total,
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

    # Create Shipment if carrier selected
    if selected_carrier:
        import uuid
        tracking_code = f"{selected_carrier.name[:3].upper()}{uuid.uuid4().hex[:8].upper()}"
        Shipment.objects.create(
            orderID=order,
            trackingCode=tracking_code,
            status="PENDING"
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
