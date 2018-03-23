import json
from pprint import pprint
from django.test import TestCase
from workflows import models
from django.test import Client


class WorkflowGetTestCase(TestCase):

    def test_success(self):
        question_type = models.QuestionType.objects.create(name='question_type')
        workflow = models.Workflow.objects.create(name='workflow_test')
        question = models.Question.objects.create(text='question_test', workflow=workflow, question_type=question_type)
        answer_type = models.AnswerType.objects.create(name='answer_type')
        answer = models.Answer.objects.create(question=question, text='answer_text', answer_type=answer_type)

        c = Client()
        response = c.get('/api/workflows/{}'.format(workflow.id))

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(
            response_data,
            {
                'workflow': {
                    'id': workflow.id,
                    'name': 'workflow_test',
                    'questions': [
                        {
                            'id': question.id,
                            'type': 'question_type',
                            'text': 'question_test',
                            'more_info': None,
                            'answers': [
                                {
                                    'id': answer.id,
                                    'image_url': None,
                                    'text': 'answer_text',
                                    'type': 'answer_type'
                                }
                            ]
                        }
                    ]
                }
            }
        )
