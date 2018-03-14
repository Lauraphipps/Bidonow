from django.db import models

# Create your models here.

class Workflow(models.Model):
    slug = models.SlugField(unique=True, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.slug


class QuestionType(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    slug = models.SlugField(null=False, blank=False)
    question_type = models.ForeignKey(QuestionType, blank=False, null=False, on_delete=models.PROTECT)
    text = models.CharField(max_length=1000, blank=False, null=False)
    workflow = models.ForeignKey(Workflow, blank=False, null=False, on_delete=models.CASCADE)
    order = models.IntegerField(blank=False, null=False)

    class Meta:
        unique_together = ('slug', 'workflow',)

    def __str__(self):
        return self.slug


class Answer(models.Model):
    slug = models.SlugField(null=False, blank=False)
    question = models.ForeignKey(Question, blank=False, null=False, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, blank=False, null=False)
    next_question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.PROTECT, related_name='next_questions')
    order = models.IntegerField(blank=False, null=False)

    class Meta:
        unique_together = ('slug', 'question',)

    def __str__(self):
        return self.slug
