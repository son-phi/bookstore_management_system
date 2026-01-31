from django.urls import path
from store.controllers.supportController.payment_controller import (
    payment_methods,
    payment_create_for_order,
    payment_detail,
    payment_confirm,
    payment_refund,
)

urlpatterns = [
    path("payment-methods/", payment_methods),

    path("orders/<int:order_id>/payments/create/", payment_create_for_order),

    path("payments/<int:payment_id>/", payment_detail),
    path("payments/<int:payment_id>/confirm/", payment_confirm),
    path("payments/<int:payment_id>/refund/", payment_refund),
]
