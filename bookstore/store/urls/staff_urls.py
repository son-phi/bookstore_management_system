from django.urls import path
from store.controllers.staffController.inventory_controller import (
    supplier_list, supplier_create,
    warehouse_list, warehouse_create,
    slip_list, slip_create, slip_detail,
    slip_add_detail, slip_remove_detail, slip_approve,
    stock_check
)
from store.controllers.staffController.staff_book_controller import (
    book_list, book_create, book_update, book_delete
)
from store.controllers.supportController.shipment_controller import (
    shipment_manage, update_status, add_trace
)

urlpatterns = [
    # Books
    path("staff/books/", book_list),
    path("staff/books/create/", book_create),
    path("staff/books/<int:book_id>/update/", book_update),
    path("staff/books/<int:book_id>/delete/", book_delete),

    # Stock Check
    path("staff/stock-check/", stock_check),

    path("staff/suppliers/", supplier_list),
    path("staff/suppliers/create/", supplier_create),

    path("staff/warehouses/", warehouse_list),
    path("staff/warehouses/create/", warehouse_create),

    path("staff/slips/", slip_list),
    path("staff/slips/create/", slip_create),
    path("staff/slips/<int:slip_id>/", slip_detail),
    path("staff/slips/<int:slip_id>/details/add/", slip_add_detail),
    path("staff/slips/<int:slip_id>/details/<int:detail_id>/remove/", slip_remove_detail),
    path("staff/slips/<int:slip_id>/approve/", slip_approve),

    # Shipment Management
    path("staff/shipments/", shipment_manage),
    path("staff/shipments/<int:shipment_id>/status/", update_status),
    path("staff/shipments/<int:shipment_id>/trace/", add_trace),
]
