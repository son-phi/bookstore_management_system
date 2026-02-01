from decimal import Decimal
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from store.models import (
    Supplier, Warehouse, ImportSlip, ImportDetail, StockEntry, Book
)
from .staff_auth import staff_login_required


# ===== Supplier =====
@staff_login_required
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by("name")
    return render(request, "staff/suppliers.html", {"suppliers": suppliers})


@staff_login_required
def supplier_create(request):
    if request.method == "GET":
        return render(request, "staff/supplier_create.html")

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    taxCode = request.POST.get("taxCode", "").strip()

    if not name:
        return render(request, "staff/supplier_create.html", {"error": "name required"})

    Supplier.objects.create(name=name, email=email, phone=phone, taxCode=taxCode)
    return redirect("/staff/suppliers/")


# ===== Warehouse =====
@staff_login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.all().order_by("name")
    return render(request, "staff/warehouses.html", {"warehouses": warehouses})


@staff_login_required
def warehouse_create(request):
    if request.method == "GET":
        return render(request, "staff/warehouse_create.html")

    name = request.POST.get("name", "").strip()
    location = request.POST.get("location", "").strip()
    capacity_raw = request.POST.get("capacity", "0").strip()

    try:
        capacity = int(capacity_raw)
    except ValueError:
        capacity = 0

    if not name:
        return render(request, "staff/warehouse_create.html", {"error": "name required"})

    Warehouse.objects.create(name=name, location=location, capacity=capacity)
    return redirect("/staff/warehouses/")


# ===== Import Slip =====
@staff_login_required
def slip_list(request):
    slips = ImportSlip.objects.select_related("warehouseID", "supplierID", "staffID").order_by("-slipID")[:50]
    return render(request, "staff/slips.html", {"slips": slips})


@staff_login_required
def slip_create(request):
    user = request.current_user

    if request.method == "GET":
        warehouses = Warehouse.objects.all().order_by("name")
        suppliers = Supplier.objects.all().order_by("name")
        return render(request, "staff/slip_create.html", {"warehouses": warehouses, "suppliers": suppliers})

    warehouse_id = request.POST.get("warehouse_id", "").strip()
    supplier_id = request.POST.get("supplier_id", "").strip()

    if not warehouse_id or not supplier_id:
        warehouses = Warehouse.objects.all().order_by("name")
        suppliers = Supplier.objects.all().order_by("name")
        return render(request, "staff/slip_create.html", {
            "warehouses": warehouses, "suppliers": suppliers, "error": "warehouse/supplier required"
        })

    wh = Warehouse.objects.get(warehouseID=int(warehouse_id))
    sp = Supplier.objects.get(supplierID=int(supplier_id))

    slip = ImportSlip.objects.create(
        warehouseID=wh,
        supplierID=sp,
        staffID=user,
        totalCost=Decimal("0.00"),
    )
    return redirect(f"/staff/slips/{slip.slipID}/")


@staff_login_required
def slip_detail(request, slip_id: int):
    slip = get_object_or_404(
        ImportSlip.objects.select_related("warehouseID", "supplierID", "staffID"),
        slipID=slip_id,
    )
    details = ImportDetail.objects.filter(slipID=slip).select_related("bookID").order_by("id")
    books = Book.objects.all().order_by("title")
    return render(request, "staff/slip_detail.html", {"slip": slip, "details": details, "books": books})


@staff_login_required
def slip_add_detail(request, slip_id: int):
    if request.method != "POST":
        return redirect(f"/staff/slips/{slip_id}/")

    slip = get_object_or_404(ImportSlip, slipID=slip_id)

    book_id = request.POST.get("book_id", "").strip()
    qty_raw = request.POST.get("quantity", "1").strip()
    cost_raw = request.POST.get("costPrice", "0").strip()

    try:
        qty = int(qty_raw)
    except ValueError:
        qty = 1

    try:
        cost = Decimal(cost_raw)
    except Exception:
        cost = Decimal("0.00")

    if not book_id or qty <= 0:
        return redirect(f"/staff/slips/{slip_id}/")

    book = Book.objects.get(bookID=int(book_id))

    ImportDetail.objects.create(
        slipID=slip,
        bookID=book,
        quantity=qty,
        costPrice=cost
    )
    return redirect(f"/staff/slips/{slip_id}/")


@staff_login_required
def slip_remove_detail(request, slip_id: int, detail_id: int):
    if request.method != "POST":
        return redirect(f"/staff/slips/{slip_id}/")

    slip = get_object_or_404(ImportSlip, slipID=slip_id)
    detail = get_object_or_404(ImportDetail, id=detail_id, slipID=slip)
    detail.delete()
    return redirect(f"/staff/slips/{slip_id}/")


@staff_login_required
def slip_approve(request, slip_id: int):
    """
    Approve slip = nhập kho thật:
    - totalCost = sum(quantity * costPrice)
    - Book.stock += quantity
    - StockEntry created
    """
    if request.method != "POST":
        return redirect(f"/staff/slips/{slip_id}/")

    user = request.current_user

    with transaction.atomic():
        slip = get_object_or_404(ImportSlip.objects.select_for_update(), slipID=slip_id)
        details = list(
            ImportDetail.objects.select_related("bookID")
            .select_for_update()
            .filter(slipID=slip)
        )
        if not details:
            return redirect(f"/staff/slips/{slip_id}/")

        total = Decimal("0.00")
        for d in details:
            total += (Decimal(d.quantity) * d.costPrice)

        # update book stock + create stock entry
        for d in details:
            Book.objects.filter(bookID=d.bookID_id).update(stock=F("stock") + d.quantity)
            StockEntry.objects.create(
                warehouseID=slip.warehouseID,
                bookID=d.bookID,
                quantity=d.quantity
            )

        slip.totalCost = total
        slip.status = "COMPLETED"
        slip.staffID = user  # đảm bảo người approve
        slip.save(update_fields=["totalCost", "staffID", "status"])

    return redirect(f"/staff/slips/{slip_id}/")


# ===== Stock Check =====
@staff_login_required
def stock_check(request):
    """
    View current stock entries in all warehouses
    """
    # Optional: Filter by warehouse
    warehouse_id = request.GET.get("warehouse", "").strip()
    
    entries = StockEntry.objects.select_related("warehouseID", "bookID").order_by("warehouseID", "bookID__title")
    
    if warehouse_id:
        entries = entries.filter(warehouseID_id=warehouse_id)
        
    warehouses = Warehouse.objects.all().order_by("name")
    
    return render(request, "staff/stock_check.html", {
        "entries": entries,
        "warehouses": warehouses,
        "selected_wh": int(warehouse_id) if warehouse_id.isdigit() else None
    })
