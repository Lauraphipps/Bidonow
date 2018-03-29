from django.urls import path, include
from . import question_type


urlpatterns = [
    path('question-type/', include(question_type.urlpatterns))
]
