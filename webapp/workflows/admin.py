from django.contrib import admin
import nested_admin
from . import models


admin.site.register(models.QuestionType)

class AnswerInline(nested_admin.NestedTabularInline):
    model = models.Answer
    fk_name = 'question'
    ordering = ['order']


class QuestionInline(nested_admin.NestedTabularInline):
    model = models.Question
    ordering = ['order']
    inlines = [
        AnswerInline
    ]



class WorkflowAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        QuestionInline
    ]


admin.site.register(models.Workflow, WorkflowAdmin)
