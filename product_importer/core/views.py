from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from rest_framework.generics import CreateAPIView

from product_importer.core.models import Product
from product_importer.core.serializers import ProductUploadSerializer


class IndexView(TemplateView):
    """ View for the default index page"""
    template_name = 'index.html'


class ProductList(ListView):
    """ View for listing of products """
    template_name = 'product_list.html'
    model = Product
    paginate_by = 10


class ProductCreateView(SuccessMessageMixin, CreateView):
    """ View for creating a product """
    template_name = 'product_form.html'
    model = Product
    fields = ['sku', 'name', 'description', 'is_active']
    success_url = reverse_lazy('product-list')
    success_message = 'Product <strong>%(name)s</strong> has been ' \
                      'created successfully'


class ProductUpdateView(SuccessMessageMixin, UpdateView):
    """ View for updating a product """
    template_name = 'product_form.html'
    model = Product
    fields = ['sku', 'name', 'description', 'is_active']
    success_url = reverse_lazy('product-list')
    success_message = 'Product <strong>%(name)s</strong> has been ' \
                      'edited successfully'


class ProductUploadView(CreateAPIView):
    serializer_class = ProductUploadSerializer
