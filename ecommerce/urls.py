"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView, RedirectView
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from analytics.views import SalesView, SalesAjaxView
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from accounts.views import LoginView, RegisterView, GuestRegisterView
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from carts.views import cart_detail_api_view
from products.views import (
    # ProductListView,
    # ProductDetailView,
    # ProductDetailSlugView,
    ProductFeaturedListView,
    ProductFeatureDetailView,
    )
from orders.views import LibraryView

from carts.views import cart_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('products/', include('products.urls', namespace='products')),
    path('search/', include('search.urls', namespace='search')),
    path('bootstrap/', TemplateView.as_view(template_name='bootstrap/example.html')),
    path('api/cart/', cart_detail_api_view, name="api-cart"),
    path('cart/', include('carts.urls', namespace='cart')),
    # path('products/', ProductListView.as_view(), name = 'product_list_view'),
    # path('products/<int:pk>/', ProductDetailView.as_view(), name = 'product_detail_view'),
    # path('products/<slug:slug>/', ProductDetailSlugView.as_view(), name = 'product_detail_view'),
    path('featured/', ProductFeaturedListView.as_view(), name = 'featured_product_list_view'),
    path('featured/<int:pk>/', ProductFeatureDetailView.as_view(), name = 'featured_product_detail_view'),
    path('login/', LoginView.as_view(), name = 'login_page'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('register/', RegisterView.as_view(), name = 'register_page'),
    path('register/guest/', GuestRegisterView.as_view(), name = 'guest_register'),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('settings/email/', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    path('webhooks/mailchimp/', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
    path('account/', include('accounts.urls', namespace='account')),
    path('accounts/', include('accounts.passwords.urls')),
    # path('accounts/login/', RedirectView.as_view(url='/login')),
    path('accounts/', RedirectView.as_view(url='/account/')),
    path('settings/', RedirectView.as_view(url='/account/')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('library/', LibraryView.as_view(), name='library'),
    path('analytics/sales/', SalesView.as_view(), name='sales-analytics'),
    path('analytics/sales/data/', SalesAjaxView.as_view(), name='sales-analytics-data'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)