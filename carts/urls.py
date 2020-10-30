from django.urls import path
from carts.views import (
    cart_home,
    cart_update,
    checkout_home,
    check_done_view,
    )

app_name = "cart"

urlpatterns = [
    path('', cart_home, name = 'home'),
    path('checkout/', checkout_home, name="checkout"),
    path('update/', cart_update, name = 'update'),
    path('checkout/success/', check_done_view, name = 'success'),
]