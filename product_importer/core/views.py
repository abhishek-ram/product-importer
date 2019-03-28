from django.views.generic import TemplateView
from django.views.generic import ListView

from product_importer.core.models import Product


class IndexView(TemplateView):
    """ View for the default index page"""
    template_name = 'index.html'


class ProductList(ListView):
    """ View for listing of products """
    template_name = 'product_list.html'
    model = Product
    paginate_by = 10

