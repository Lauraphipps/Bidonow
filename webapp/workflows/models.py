from django.db import models

# Create your models here.

class WorkflowCategory(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class QuestionBundle(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)


class Workflow(QuestionBundle):
    image = models.ImageField(null=True, blank=True, upload_to='workflows/workflows/')
    category = models.ForeignKey(WorkflowCategory, blank=True, null=True,  on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def clone(self, **kwargs):
        fields = ('name', 'description', 'image', 'category')
        nw = Workflow()
        for f in fields:
            setattr(nw, f, getattr(self, f))
        for name, value in kwargs.items():
            setattr(nw, name, value)
        nw.save()
        for q in self.question_set.all():
            nq = q.clone(bundle=nw)
        return nw


class QuestionType(QuestionBundle):
    # is_bundle = models.BooleanField(null=False, blank=False, default=False)
    def __str__(self):
        return self.name

    @property
    def is_bundle(self):
        return self.question_set.exists()


class Question(models.Model):
    question_type = models.ForeignKey(QuestionType, blank=False, null=False, on_delete=models.PROTECT, related_name='ref_questions')
    text = models.CharField(max_length=1000, blank=False, null=False)
    bundle = models.ForeignKey(QuestionBundle, blank=False, null=False, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='workflows/questions/')
    order = models.IntegerField(blank=True, null=True)
    optional = models.BooleanField(blank=False, null=False, default=False)
    more_info = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.text

    def clone(self, **kwargs):
        fields = ('question_type', 'text', 'bundle', 'image', 'order', 'optional', 'more_info')
        new_obj = Question()
        for f in fields:
            setattr(new_obj, f, getattr(self, f))
        for name, value in kwargs.items():
            setattr(new_obj, name, value)
        new_obj.save()

        for ans in self.answer_set.all():
            ans.clone(question=new_obj)

        return new_obj


class AnswerType(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.ForeignKey(Question, blank=False, null=False, on_delete=models.CASCADE)
    answer_type = models.ForeignKey(AnswerType, blank=True, null=True, on_delete=models.PROTECT)
    text = models.CharField(max_length=1000, blank=False, null=False)
    next_question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.PROTECT, related_name='next_questions')
    image = models.ImageField(null=True, blank=True, upload_to='workflows/answers/')
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.text

    def clone(self, **kwargs):
        fields = ('question', 'answer_type', 'text', 'next_question', 'image', 'order')
        new_obj = Answer()
        for f in fields:
            setattr(new_obj, f, getattr(self, f))
        for name, value in kwargs.items():
            setattr(new_obj, name, value)
        new_obj.save()
        return new_obj
