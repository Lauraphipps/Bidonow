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
import workflows.urls
import bn_auth.urls


from . import views

urlpatterns = [
    path('', views.home),
    path('upload-file/', views.upload_file),
    path('make-bid/<int:bid_id>/', views.make_bid),
    path('api/workflows/<int:bid_id>', views.api_get_bid),
    path('api/workflowcategory/', views.api_workflowcategory_list),

    path('api/workflow/', views.api_workflow_items),
    path('api/workflow/<int:workflow_id>/', views.api_workflow_item),
    path('api/workflow/save', views.api_workflow_save),
    path('api/workflow/delete', views.api_workflow_delete),
    path('api/workflow/clone', views.api_workflow_clone),


    path('api/bundle/<int:bundle_id>/questions/', views.api_bundel_questions),

    path('api/question-types/', views.api_question_types),
    path('api/question/<int:question_id>/', views.api_question_get),
    path('api/question/save', views.api_question_save),
    path('api/question/delete', views.api_question_delete),

    path('api/answer-types/', views.api_answer_types),
    path('api/answer/<int:answer_id>/', views.api_answer_get),
    path('api/answer/save', views.api_answer_save),
    path('api/answer/delete', views.api_answer_delete),

    path('admin/control-panel/', views.control_panel),
    path('admin/raw-sql/', views.raw_sql),
    path('admin/', admin.site.urls),
    path(r'nested_admin/', include('nested_admin.urls')),
    path('api/workflows/', include(workflows.urls)),
    path('api/auth/', include(bn_auth.urls)),
]


if settings.INSTANCE_TYPE == 'dev':
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
