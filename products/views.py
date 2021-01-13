import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect

from analytics.mixins import ObjectViewedMixin
from carts.models import Cart

from .models import Product, ProductFile

class ProductFeaturedListView(ListView):
    # model = Product
    template_name = "product/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductFeatureDetailView(ObjectViewedMixin, DetailView):
    # model = Product
    template_name = "product/featured-detail.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class UserProductHistoryView(LoginRequiredMixin, ListView):
    # model = Product
    template_name = "product/user-history.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, model_queryset=False)
        return views

class ProductListView(ListView):
    # model = Product
    template_name = "product/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    # model = Product
    template_name = "product/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")
        
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found...")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance

from wsgiref.util import FileWrapper
from mimetypes import guess_type

from django.conf import settings
from orders.models import ProductPurchase

class ProductDownloadView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("Downloads not found")
        download_obj = downloads_qs.first()
        purchased_products = Product.objects.none()
        can_download = False
        user_ready = True

        if download_obj.user_required:
            if not request.user.is_authenticated:
                user_ready = False

        if download_obj.free:
            can_download = True
            user_ready = True
        else:
            purchased_products = ProductPurchase.objects.product_by_request(request)
            if download_obj.product in purchased_products:
                can_download = True
        
        if not can_download or not user_ready:
            messages.error(request, "You do not have access to download this item.")
            return redirect(download_obj.get_default_url())

        aws_filepath = download_obj.generate_download_url()
        print(aws_filepath)
        return HttpResponseRedirect(aws_filepath)
        # file_root = settings.PROTECTED_ROOT
        # filepath = download_obj.file.path
        # final_filepath = os.path.join(file_root, filepath)
        # with open(final_filepath, 'rb') as f:
        #     wrapper = FileWrapper(f)
        #     mimetype = 'application/force-download'
        #     gussed_mimetype = guess_type(filepath)[0]
        #     if gussed_mimetype:
        #         mimetype = gussed_mimetype
        #     response = HttpResponse(wrapper, content_type=mimetype)
        #     response['Content-Disposition'] = "attachment;filename={filename}".format(filename=download_obj.name)
        #     response['X_SendFile'] = str(download_obj.name)
        #     return response

class ProductDetailView(DetailView):
    # model = Product
    template_name = "product/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(id=pk)