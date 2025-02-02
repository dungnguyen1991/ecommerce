from django.urls import path, re_path

from products.views import UserProductHistoryView
from .views import (
    OrderListView,
    OrderDetailView,
    VerifyOwnership,
    )

app_name = "orders"

urlpatterns = [
    path('', OrderListView.as_view(), name = 'list'),
    path('endpoint/verify/ownership/', VerifyOwnership.as_view(), name = 'verify-ownership'),
    path('<slug:order_id>/', OrderDetailView.as_view(), name="detail"),
]