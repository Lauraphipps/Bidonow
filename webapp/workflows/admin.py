from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
import nested_admin
from . import models


admin.site.register(models.QuestionType)
admin.site.register(models.AnswerType)
admin.site.register(models.WorkflowCategory)


class FormSetWithParent(forms.BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super(FormSetWithParent, self).get_form_kwargs(index)
        kwargs.update({'parent': self.instance})
        return kwargs


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        parent_question = kwargs.pop('parent')
        super(AnswerForm, self).__init__(*args, **kwargs)
        if self.instance and parent_question and parent_question.pk is not None: # Editing and existing instance
            next_question_field = self.fields['next_question']
            workflow =parent_question.workflow
            next_question_field.queryset = models.Question.objects.filter(workflow=workflow)


class AnswerInline(nested_admin.NestedTabularInline):
    model = models.Answer
    fk_name = 'question'
    ordering = ['order', 'id']
    extra = 0
    form = AnswerForm
    formset = FormSetWithParent

    def render_change_form111(self, request, context, *args, **kwargs):
        print('instance: {}'.format(self.instance))
        context['adminform'].form.fields['next_question'].queryset = models.Question.objects.filter(workflow=obj.question.workflow)
        return super(AnswerInline, self).render_change_form(request, context, *args, **kwargs)


class QuestionInline(nested_admin.NestedTabularInline):
    model = models.Question
    ordering = ['order', 'id']
    inlines = [
        AnswerInline
    ]
    extra = 0



class WorkflowAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        QuestionInline
    ]
    readonly_fields = ('object_link',)
    class Media:
        css = {
             'all': ('workflows/admin/workflow.css',)
        }

    def object_link(self, obj):
        url = '/make-bid/{}/'.format(obj.id)
        print(url)
        return mark_safe('<a href="{}">{}</a>'.format(url, url))

    object_link.short_description = "Check on site"


admin.site.register(models.Workflow, WorkflowAdmin)
