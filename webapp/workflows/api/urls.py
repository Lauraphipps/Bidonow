from django.urls import path, include
from . import question_type
from . import workflow_category


urlpatterns = [
    path('question-type/', include(question_type.urlpatterns)),
    path('workflow-category/', include(workflow_category.urlpatterns))
]
