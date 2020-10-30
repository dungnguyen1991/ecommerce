from django.urls import path
from .views import home_page, about_page, contact_page

urlpatterns = [
    path('', home_page, name = 'home'),
    path('about/', about_page, name = 'about_page'),
    path('contact/', contact_page, name = 'contact_page'),
]