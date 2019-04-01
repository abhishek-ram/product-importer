"""product_importer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import django_eventstream

from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from product_importer.core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Product Importer urls
    path('index/', core_views.IndexView.as_view(), name='index'),
    path('products/', core_views.ProductListView.as_view(), name='product-list'),
    path('products/create/', core_views.ProductCreateView.as_view(),
         name='product-create'),
    path('products/<int:pk>/edit', core_views.ProductUpdateView.as_view(),
         name='product-update'),
    path('products/upload/', core_views.ProductUploadView.as_view(),
         name='product-upload'),
    path('event-hooks/', core_views.EventHookListView.as_view(),
         name='eventhook-list'),
    path('event-hooks/create/', core_views.EventHookCreateView.as_view(),
         name='eventhook-create'),
    path('event-hooks/<int:pk>/edit', core_views.EventHookUpdateView.as_view(),
         name='eventhook-update'),
    path('event-hooks/<int:pk>/edit', core_views.EventHookUpdateView.as_view(),
         name='eventhook-update'),

    path('import-events/', include(django_eventstream.urls),
         {'channels': ['product-import']}),

    path('uploads/sign-s3/', core_views.UploadsSignS3View.as_view(),
         name='uploads-sign-s3'),

    # Default all other urls to index view
    re_path(r'^.*', core_views.IndexView.as_view()),
]
