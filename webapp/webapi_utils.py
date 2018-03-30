import collections
import json
from django.http import JsonResponse
from django.urls import path, include
from django.db import models as django_models
from django.views.decorators.csrf import csrf_exempt

__all__ = ['UrlRegister', 'to_dict', 'update_model', 'RestHandler']


class RestHandler(object):
    def __init__(self, model_class):
        self.model_class = model_class

    @csrf_exempt
    def list_dispacher(self, request):
        if request.method == 'GET':
            return self.list_get(request)
        if request.method == 'POST':
            return self.list_save(request)
        raise Exception('Can nof find handler for method: {}'.format(request.method))

    def list_get(self, request):
        raise NotImplementedError()

    def list_save(self, request):
        data = json.loads(request.body)
        if data.get('id') and data.get('id') > 0:
            model = self.model_class.objects.get(id=data.get('id'))
        else:
            model = self.model_class()
        update_model(model, data)
        model.save()
        return JsonResponse(to_dict(model))

    @csrf_exempt
    def item_dispacher(self, request, item_id):
        if request.method == 'GET':
            return self.item_get(request, item_id)
        if request.method == 'DELETE':
            return self.item_delete(request, item_id)

        raise Exception('Can nof find handler for method: {}'.format(request.method))

    def item_get(self, request, item_id):
        model = self.model_class.objects.get(id=item_id)
        return JsonResponse(to_dict(model))


    def item_delete(self, request, item_id):
        model = self.model_class.objects.get(id=item_id)
        model.delete()
        return JsonResponse({})


    def get_urls(self):
        return [
            path('rest/', self.list_dispacher),
            path('rest/<int:item_id>/', self.item_dispacher)
        ]




class UrlRegister(object):
    def __init__(self):
        self._routes = []

    def add(self, pattern):
        def decorator(func):
            self._routes.append((pattern, func))
            return func
        return decorator

    def get_paths(self):
        result = [
            path(r[0], r[1])
            for r in self._routes
        ]
        return result


def to_dict(obj, extra=None):
    if isinstance(obj, collections.Iterable):
        return models_to_list(obj, extra=extra)
    return model_to_dict(obj, extra=extra)


def model_to_dict(obj, extra=None):
    fields = obj._meta.get_fields()
    data = {}
    for field in fields:
        add_field_value(data, obj, field)
    if extra is not None:
        for name, func in extra.items():
            print('obj={}'.format(type(obj)))
            if isinstance(obj, models.Answer):
                print('answer_type={}'.format(obj.answer_type))
            data[name] = func(obj)
    return data


def models_to_list(objects, extra=None):
    return [
        model_to_dict(obj, extra=extra) for obj in objects
    ]


def add_field_value(data, obj, field):
    if isinstance(field, django_models.ForeignKey):
        field_name = '{}_id'.format(field.name)
        data[field_name] = getattr(obj, field_name)
    if field.is_relation:
        return
    if isinstance(field, django_models.ImageField):
        return
    data[field.name] = getattr(obj, field.name)


def update_model(obj, data):
    fields = obj._meta.get_fields()
    for f in fields:
        set_field_for_model(obj, f, data)


def set_field_for_model(obj, field, data):
    field_name = field.name
    if isinstance(field, django_models.ForeignKey):
        field_name = '{}_id'.format(field.name)
    if field_name in data:
        setattr(obj, field_name, data[field_name])
