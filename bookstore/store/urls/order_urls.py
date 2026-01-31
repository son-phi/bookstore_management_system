from django.urls import path
from store.controllers.orderController.cart_controller import (
    cart_view, cart_add, cart_inc, cart_dec, cart_set_qty, cart_remove
)
from store.controllers.orderController.checkout_controller import checkout, order_detail

urlpatterns = [
    path("cart/", cart_view),
    path("cart/add/<int:book_id>/", cart_add),
    path("cart/inc/<int:item_id>/", cart_inc),
    path("cart/dec/<int:item_id>/", cart_dec),
    path("cart/set/<int:item_id>/", cart_set_qty),
    path("cart/remove/<int:item_id>/", cart_remove),

    path("checkout/", checkout),
    path("orders/<int:order_id>/", order_detail),
]
