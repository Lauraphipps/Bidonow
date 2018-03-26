from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from workflows.models import Workflow
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import uuid
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def raw_sql(request):
    sql_str = request.POST.get('sql_str', '')
    result = None
    if sql_str:
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            rows = cursor.fetchall()
            fields = [field[0] for field in cursor.description]
            result = {
                'fields': fields,
                'rows': rows
            }
    return render(request, 'raw-sql.html', {'result': result, 'sql_str': sql_str})


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
        'type': a.answer_type.name if a.answer_type is not None else None,
        'image_url': a.image.url if a.image else None
    }


def _format_question(q):
    return {
        'id': q.id,
        'text': q.text,
        'type': q.question_type.name,
        'answers': [_format_answer(a) for a in q.answer_set.all()],
        'more_info': q.more_info
    }


def _get_questions_for_bundle(bundle):
    questions = list(bundle.question_set.all())
    for q in questions:
        if not q.question_type.is_bundle: 
            yield q
        else:
            for q1 in _get_questions_for_bundle(q.question_type):
                yield q1


def api_get_bid(request, bid_id):
    workflow = Workflow.objects.get(id=bid_id)
    workflow_data = {
        'id': workflow.id,
        'name': workflow.name,
        'questions': [_format_question(q) for q in _get_questions_for_bundle(workflow)]
    }
    data = {
        'workflow': workflow_data
    }
    return JsonResponse(data)
