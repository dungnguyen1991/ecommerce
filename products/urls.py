from django.urls import path
from products.views import (
    ProductListView,
    ProductDetailSlugView,
    ProductDownloadView,
    )

app_name = "products"

urlpatterns = [
    path('', ProductListView.as_view(), name = 'product_list_view'),
    # path('products/<int:pk>/', ProductDetailView.as_view(), name = 'product_detail_view'),
    path('<slug:slug>/', ProductDetailSlugView.as_view(), name = 'product_detail_view'),
    path('<slug:slug>/<int:pk>/', ProductDownloadView.as_view(), name = 'download'),
]