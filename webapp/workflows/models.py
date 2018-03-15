from django.db import models

# Create your models here.

class Workflow(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class QuestionType(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_type = models.ForeignKey(QuestionType, blank=False, null=False, on_delete=models.PROTECT)
    text = models.CharField(max_length=1000, blank=False, null=False)
    workflow = models.ForeignKey(Workflow, blank=False, null=False, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, blank=False, null=False, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, blank=False, null=False)
    next_question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.PROTECT, related_name='next_questions')
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.text
