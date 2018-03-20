from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from workflows.models import Workflow
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import uuid



def home(request):
    return render(request, 'home.html')


def make_bid(request, bid_id):
    data = {
        'workflow_id': bid_id
    }
    return render(request, 'make-bid.html', data)


@csrf_exempt
def upload_file(request): 
    if request.method == 'POST':
        f = request.FILES['file1']
        file_name = '{}{}'.format(str(uuid.uuid4()), os.path.splitext(f.name)[1])
        path = os.path.join(settings.MEDIA_ROOT, 'tmp',  file_name)
        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    return JsonResponse({})


def _format_answer(a):
    return {
        'id': a.id,
        'text': a.text,
        'type': a.answer_type.name if a.answer_type is not None else None
    }


def _format_question(q):
    return {
        'id': q.id,
        'text': q.text,
        'type': q.question_type.name,
        'answers': [_format_answer(a) for a in q.answer_set.all()]
    }


def api_get_bid(request, bid_id):
    workflow = Workflow.objects.get(id=bid_id)
    workflow_data = {
        'id': workflow.id,
        'name': workflow.name,
        'questions': [_format_question(q) for q in workflow.question_set.all()]
    }
    data = {
        'workflow': workflow_data
    }
    return JsonResponse(data)
