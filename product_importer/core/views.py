import boto3
import django_filters
from botocore.client import Config
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django_filters.views import FilterView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from product_importer.core.models import EventHook
from product_importer.core.models import Product
from product_importer.core.models import ProductUpload
from product_importer.core.serializers import ProductUploadSerializer


class IndexView(TemplateView):
    """ View for the default index page"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """ Update the context for this page"""
        context = super().get_context_data(**kwargs)
        context['current_upload'] = ProductUpload.objects.\
            filter(is_active=True).first()
        context['last_upload'] = ProductUpload.objects.\
            filter(is_active=False).order_by('-started_at').first()
        return context


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
    success_url = reverse_lazy('index')


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


class UploadsSignS3View(GenericAPIView):
    """ View for signing of s3 upload requests from frontend """

    def get(self, request):
        s3 = boto3.client('s3', region_name='ap-south-1',
                          config=Config(signature_version='s3v4'))
        signed_post = s3.generate_presigned_post(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key='product_data/' + request.GET['file_name'],
            Fields={"acl": "public-read",
                    "Content-Type": request.GET['file_type']},
            Conditions=[
                {"acl": "public-read"},
                {"Content-Type": request.GET['file_type']}
            ],
            ExpiresIn=3600
        )
        return Response(
            {'data': signed_post,
             'url': f'https://{settings.AWS_STORAGE_BUCKET_NAME}.'
                    f's3.amazonaws.com/{request.GET["file_name"]}'
             }
        )
