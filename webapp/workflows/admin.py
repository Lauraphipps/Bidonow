from django.contrib import admin
from . import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe


admin.site.register(models.QuestionType)
admin.site.register(models.Answer)


class QuestionInline(admin.TabularInline):
    model = models.Question
    ordering = ['order']
    readonly_fields = ('_link', )

    def _link(self, obj):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            return mark_safe("""<a href="{url}">{text}</a>""".format(
                url=url,
                text=_("Edit"),
            ))
        return _("-")



class WorkflowAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline
    ]


admin.site.register(models.Workflow, WorkflowAdmin)


class AnswerInline(admin.TabularInline):
    model = models.Answer
    fk_name = 'question'
    ordering = ['order']


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline
    ]


admin.site.register(models.Question, QuestionAdmin)
