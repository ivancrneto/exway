import base64
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse as r


class ExpensesAPITest(TestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'Ivan',
            'last_name': 'Neto',
            'username': 'ivancrneto',
            'email': 'ivan.cr.neto@me.com',
            'password': '123456',
        }
        self.create_user()

        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +\
            base64.b64encode('{}:{}'.format(self.user.username,
                                            self.user_data['password']))
        }

    def create_user(self, **kwargs):
        data = self.user_data
        data.update(**kwargs)
        self.user = User(**data)
        self.user.set_password(data['password'])
        self.user.save()

    def test_get_expenses_no_auth(self):
        """ Not authenticated requests should get an 403 reponse """
        resp = self.client.get(r('core:expenses'))
        self.assertEqual(403, resp.status_code)

    def test_get_expenses_auth(self):
        """ Authenticated requests should get an 200 reponse """
        resp = self.client.get(r('core:expenses'), **self.auth_headers)
        self.assertEqual(200, resp.status_code)

