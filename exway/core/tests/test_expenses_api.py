import base64
import json
import pytz
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse as r
from exway.core.models import Expense


class ExpensesAPITestBase(TestCase):
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

    def create_expense(self, user, **kwargs):

        expense_data = {
            'description': 'A new TV for my bedroom',
            'datetime': datetime.now(tz=pytz.UTC),
            'amount': 700,
            'comment': 'my old one is broken',
        }
        expense_data.update(**kwargs)
        expense = Expense(**expense_data)
        expense.user = user
        expense.save()
        return expense


class ExpensesAPITestGet(ExpensesAPITestBase):
    def test_get_expenses_no_auth(self):
        """ Not authenticated requests should get an 403 reponse """
        resp = self.client.get(r('core:expenses'))
        self.assertEqual(403, resp.status_code)

    def test_get_expenses_auth(self):
        """ Authenticated requests should get an 200 reponse """
        resp = self.client.get(r('core:expenses'), **self.auth_headers)
        self.assertEqual(200, resp.status_code)

    def test_get_show_users_expenses(self):
        """ Get should show all users saved expenses """
        # creating two expenses
        expense1 = self.create_expense(self.user)
        expense2 = self.create_expense(self.user,
                                       description='A cheap TV for my son',
                                       amount=300, comment='')

        resp = self.client.get(r('core:expenses'), **self.auth_headers)
        resp = json.loads(resp.content)
        self.assertEquals(2, len(resp))
        self.assertEquals({expense1.id, expense2.id},
                          {i['id'] for i in resp})
        self.assertEquals({expense1.amount, expense2.amount},
                          {float(i['amount']) for i in resp})


class ExpensesAPITestPost(ExpensesAPITestBase):
    def setUp(self):
        self.expense_data = {
            'description': 'A new TV for my bedroom',
            'date': datetime.now(tz=pytz.UTC).strftime('%Y-%m-%d'),
            'time': datetime.now(tz=pytz.UTC).strftime('%I:%M %p'),
            'amount': 700,
            'comment': 'my old one is broken',
        }

        ExpensesAPITestBase.setUp(self)

    def test_post_expense(self):
        """ Good post should return 201 created status and expense data """

        resp = self.client.post(r('core:expenses'), self.expense_data,
                                **self.auth_headers)
        self.assertEquals(201, resp.status_code)
        resp = json.loads(resp.content)
        extra_keys = ['id', 'user', 'created_on']
        self.assertListEqual(sorted(self.expense_data.keys() + extra_keys),
                             sorted(resp.keys()))

    def test_post_missing_data(self):
        """ Posting with missing data should return 400 bad request as status \
            code """
        expense_data = self.expense_data.copy()
        del expense_data['time']
        resp = self.client.post(r('core:expenses'), expense_data,
                                **self.auth_headers)
        self.assertEquals(400, resp.status_code)
