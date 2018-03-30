import json
from django.http import JsonResponse
import webapi_utils
from workflows import models
from django.urls import path, include


router = webapi_utils.UrlRegister()
model_class = models.QuestionType


@router.add('views/list')
def question_type_list(request):
    data = {
        'items': webapi_utils.to_dict(models.QuestionType.objects.all())
    }
    return JsonResponse(data)


rest_handler = webapi_utils.RestHandler(model_class)
urlpatterns = router.get_paths() + rest_handler.get_urls()
