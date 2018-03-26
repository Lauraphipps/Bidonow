"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from . import views

urlpatterns = [
    path('', views.home),
    path('upload-file/', views.upload_file),
    path('make-bid/<int:bid_id>/', views.make_bid),
    path('api/workflows/<int:bid_id>', views.api_get_bid),
    path('admin/raw-sql/', views.raw_sql),
    path('admin/', admin.site.urls),
    path(r'nested_admin/', include('nested_admin.urls')),
]


if settings.INSTANCE_TYPE == 'dev':
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
