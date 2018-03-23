import json
from pprint import pprint
from django.test import TestCase
from workflows import models
from django.test import Client
import partial_assert as pa
from workflows.tests.helpers import factories as f


class WorkflowGetTestCase(TestCase, pa.TestCaseMixin):
    def __init__(self, *args, **kwards):
        super(WorkflowGetTestCase, self).__init__(*args, **kwards)
        pa.register_test_case(self)

    def call_api(self, workflow_id):
        c = Client()
        response = c.get('/api/workflows/{}'.format(workflow_id))
        return response

    def assertApiResponse(self, response, expected):
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertPartial(response_data, expected)

    def test_success(self):
        question_type = f.QuestionType(name='question_type')
        workflow = f.Workflow(name='workflow_test')
        question = f.Question(text='question_test', bundle=workflow, question_type=question_type)
        answer_type = f.AnswerType(name='answer_type')
        answer = f.Answer(question=question, text='answer_text', answer_type=answer_type)

        c = Client()
        response = c.get('/api/workflows/{}'.format(workflow.id))

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertPartial(
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

    def test_with_complext_question_type(self):
        simple_question_type = f.QuestionType(name='simple')
        complex_question_type = f.QuestionType()
        complex_question = f.Question(bundle=complex_question_type, question_type=simple_question_type)
        workflow = f.Workflow()
        question = f.Question(question_type=complex_question_type, bundle=workflow)

        response = self.call_api(workflow.id)

        self.assertApiResponse(
            response,
            {
                'workflow': {
                    'id': workflow.id,
                    'questions': [{'id': complex_question.id}]
                }
            }
        )
