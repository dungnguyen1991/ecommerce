from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product

class SearchProductView(ListView):
    # model = Product
    template_name = "search/view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()
        '''
        __icontains = field contains this
        __iexact = field is exactly this
        '''
