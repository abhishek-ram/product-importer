import django_filters
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django_filters.views import FilterView
from rest_framework.generics import CreateAPIView

from product_importer.core.models import EventHook
from product_importer.core.models import Product
from product_importer.core.serializers import ProductUploadSerializer


class IndexView(TemplateView):
    """ View for the default index page"""
    template_name = 'index.html'


class ProductFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_by_query')
    active_only = django_filters.CharFilter(method='filter_by_active')

    @staticmethod
    def filter_by_query(queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(sku__icontains=value) |
            Q(description__icontains=value)
        )

    @staticmethod
    def filter_by_active(queryset, name, value):
        if value == 'on':
            return queryset.filter(is_active=True)
        return queryset

    class Meta:
        model = Product
        fields = ['is_active']


class ProductListView(FilterView):
    """ View for listing of products """
    template_name = 'product_list.html'
    model = Product
    filterset_class = ProductFilter
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


class EventHookListView(ListView):
    """ View for listing of Event Hooks """
    template_name = 'eventhook_list.html'
    model = EventHook
    paginate_by = 10


class EventHookCreateView(SuccessMessageMixin, CreateView):
    """ View for creating an event hook """
    template_name = 'eventhook_form.html'
    model = EventHook
    fields = ['event_type', 'endpoint']
    success_url = reverse_lazy('eventhook-list')
    success_message = 'Event Hook has been created successfully'


class EventHookUpdateView(SuccessMessageMixin, UpdateView):
    """ View for updating an eventhooks """
    template_name = 'eventhook_form.html'
    model = EventHook
    fields = ['event_type', 'endpoint']
    success_url = reverse_lazy('eventhook-list')
    success_message = 'Event Hook has been edited successfully'

