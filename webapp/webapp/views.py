from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from workflows.models import Workflow
from workflows import models
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import uuid
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files import File as DjangoFile
from django.db import models as django_models


@staff_member_required
def control_panel(request):
    return render(request, 'control-panel/home.html', {})


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


def api_workflowcategory_list(request):
    items = [
        {'id': r.id, 'name': r.name} for r in models.WorkflowCategory.objects.all()
    ]
    data = {
        'workflowcategories': items
    }
    return JsonResponse(data)


def api_workflow_items(request):
    category_id = request.GET.get('category_id')
    qs = models.Workflow.objects.all()
    if category_id:
        qs = qs.filter(category__id=category_id)
    items = [
        {
            'id': r.id,
            'name': r.name,
            'description': r.description,
            'category_id': r.category_id, 
            'category_name': r.category.name if r.category else None
        } for r in qs
    ]
    data = {
        'workflow_items': items
    }
    return JsonResponse(data)


def object_to_dict(obj, extra=None):
    fields = obj._meta.get_fields()
    data = {}
    for field in fields:
        add_field_value(data, obj, field)
    if extra is not None:
        for name, func in extra.items():
            data[name] = func(obj)
    return data


def objects_to_list(objects, extra=None):
    return [
        object_to_dict(obj, extra=extra) for obj in objects
    ]

def add_field_value(data, obj, field):
    if field.is_relation:
        return
    if isinstance(field, django_models.ImageField):
        return
    data[field.name] = getattr(obj, field.name)


def api_workflow_item(request, workflow_id):
    w = models.Workflow.objects.get(id=workflow_id)
    item = {
        'id': w.id,
        'name': w.name,
        'description': w.description,
        'questions': objects_to_list(
            w.question_set.all(),
            extra={'answers': lambda q: objects_to_list(q.answer_set.all())}
        )
    }

    data = {
        'workflow': item
    }
    return JsonResponse(data)


@csrf_exempt
def api_workflow_save(request):
    data = json.loads(request.body)
    # {'id': 21, 'name': 'Aerial Photography', 'description': '', 'category_id': 1, 'category_name': 'Video', 'category': {'id': 1, 'name': 'Video'}}
    if data.get('id'):
        w = Workflow.objects.get(id=data['id'])
    else:
        w = Workflow()
    w.name = data['name']
    w.description = data.get('description')
    if data.get('category_id'):
        w.category_id = data['category_id']
    w.save()

    return JsonResponse({'success': True})


@csrf_exempt
def api_workflow_delete(request):
    data = json.loads(request.body)
    workflow_id = data['id']
    w = Workflow.objects.get(id=workflow_id)
    w.delete()
    return JsonResponse({'success': True})


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
