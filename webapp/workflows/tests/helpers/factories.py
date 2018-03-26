import factory
from workflows import models


def get_related(obj):
    if hasattr(obj, '_related'):
        return obj._related
    return {}


def set_related(obj, name, value):
    if not hasattr(obj, '_related'):
        setattr(obj, '_related', {})
    obj._related[name] = value


class Generator(object):
    def __init__(self):
        self.counter = 0

    def __call__(self):
        self.counter += 1
        return self.counter

id = Generator()


class BaseModelOptions(factory.django.DjangoOptions):
    def _build_default_options(self):
        return super(BaseModelOptions, self)._build_default_options()
        # + [factory.base.OptionDefault('lazy_saver', LazySaver, inherit=True),]



class BaseModelFactory(factory.django.DjangoModelFactory):
    _options_class = BaseModelOptions
    class Meta:
        abstract = True


class Workflow(BaseModelFactory):
    class Meta:
        model = models.Workflow

    name = factory.Sequence(lambda n: 'Workflow {}'.format(n))


class Question(BaseModelFactory):
    class Meta:
        model = models.Question


class QuestionType(BaseModelFactory):
    class Meta:
        model = models.QuestionType


class AnswerType(BaseModelFactory):
    class Meta:
        model = models.AnswerType


class Answer(BaseModelFactory):
    class Meta:
        model = models.Answer
