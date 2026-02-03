from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from store.models import Shipment, ShippingTrace, Order
from store.controllers.customerController.auth_helpers import staff_required

@staff_required
def shipment_manage(request):
    # filter by status or code
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    
    shipments = Shipment.objects.select_related("orderID", "orderID__userID").order_by("-shipmentID")
    
    if q:
        shipments = shipments.filter(trackingCode__icontains=q)
    if status:
        shipments = shipments.filter(status=status)

    return render(request, "staff/shipment_manage.html", {
        "shipments": shipments,
        "q": q,
        "selected_status": status
    })

@staff_required
def update_status(request, shipment_id):
    shipment = get_object_or_404(Shipment, shipmentID=shipment_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status:
            shipment.status = new_status
            shipment.save()
            
            # Auto add trace
            ShippingTrace.objects.create(
                shipmentID=shipment,
                location="Warehouse", # generic for demo
                status=new_status,
                time=timezone.now()
            )
            
    return redirect("/staff/shipments/")

@staff_required
def add_trace(request, shipment_id):
    shipment = get_object_or_404(Shipment, shipmentID=shipment_id)
    if request.method == "POST":
        location = request.POST.get("location")
        status = request.POST.get("status")
        if location and status:
            ShippingTrace.objects.create(
                shipmentID=shipment,
                location=location,
                status=status,
                time=timezone.now()
            )
    return redirect("/staff/shipments/")
