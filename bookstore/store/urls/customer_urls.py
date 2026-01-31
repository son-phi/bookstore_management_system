from django.urls import path
from store.controllers.customerController.auth_controller import register, login, logout
from store.controllers.customerController.profile_controller import profile_view, profile_update, address_add
from store.controllers.customerController.wishlist_controller import wishlist_view, wishlist_add, wishlist_remove

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("logout/", logout),

    path("profile/", profile_view),
    path("profile/update/", profile_update),
    path("profile/address/add/", address_add),

    path("wishlist/", wishlist_view),
    path("wishlist/add/<int:book_id>/", wishlist_add),
    path("wishlist/remove/<int:item_id>/", wishlist_remove),
]
