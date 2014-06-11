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
        self.user = self.create_user()

        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' +\
            base64.b64encode('{}:{}'.format(self.user.username,
                                            self.user_data['password']))
        }

    def create_user(self, **kwargs):
        data = self.user_data
        data.update(**kwargs)
        user = User(**data)
        user.set_password(data['password'])
        user.save()
        return user

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

        expenses_count = Expense.objects.count()
        resp = self.client.post(r('core:expenses'), self.expense_data,
                                **self.auth_headers)
        self.assertEquals(201, resp.status_code)
        resp = json.loads(resp.content)
        extra_keys = ['id', 'user', 'created_on']
        self.assertListEqual(sorted(self.expense_data.keys() + extra_keys),
                             sorted(resp.keys()))
        self.assertEquals(expenses_count + 1, Expense.objects.count())

    def test_post_missing_data(self):
        """ Posting with missing data should return 400 bad request as status \
            code """
        expense_data = self.expense_data.copy()
        del expense_data['time']
        resp = self.client.post(r('core:expenses'), expense_data,
                                **self.auth_headers)
        self.assertEquals(400, resp.status_code)


class ExpensesAPITestPut(ExpensesAPITestBase):
    def setUp(self):
        ExpensesAPITestBase.setUp(self)

        self.expense1 = self.create_expense(self.user)
        user2 = self.create_user(username='Paula', email='paula@gmail.com')
        self.expense2 = self.create_expense(user2)

        self.expense_data = {
            'description': 'A new TV for my bedroom',
            'date': datetime.now(tz=pytz.UTC).strftime('%Y-%m-%d'),
            'time': datetime.now(tz=pytz.UTC).strftime('%I:%M %p'),
            'amount': '700',
            'comment': 'my old one is broken',
        }

        self.auth_headers.update(
            CONTENT_TYPE='application/json; charset=utf-8')


    def test_put_expense(self):
        """ Good put request should return status code 200, and expense data \
            with updated fields """
        expense_data = self.expense_data.copy()
        expense_data['time'] = '10:10 PM'
        expense_data['comment'] = ''
        resp = self.client.put(r('core:expense_detail',
                                 kwargs={'pk': self.expense1.id}),
                               json.dumps(expense_data), **self.auth_headers)
        self.assertEquals(200, resp.status_code)
        resp = json.loads(resp.content)
        expense_data['time'] = '22:10:00'
        self.assertDictContainsSubset(expense_data, resp)

    def test_put_bad_data(self):
        """ Bad put request should return status code 400 bad request """
        expense_data = self.expense_data.copy()
        expense_data['amount'] = ''
        del expense_data['description']
        resp = self.client.put(r('core:expense_detail',
                                 kwargs={'pk': self.expense1.id}),
                               json.dumps(expense_data), **self.auth_headers)
        self.assertEquals(400, resp.status_code)

    def test_put_different_user(self):
        """ Put to a expense from a different user should return status code \
            403 forbidden """
        expense_data = self.expense_data.copy()
        resp = self.client.put(r('core:expense_detail',
                                 kwargs={'pk': self.expense2.id}),
                               json.dumps(expense_data), **self.auth_headers)
        self.assertEquals(403, resp.status_code)


class ExpensesAPITestDelete(ExpensesAPITestBase):
    def setUp(self):
        ExpensesAPITestBase.setUp(self)

        self.expense1 = self.create_expense(self.user)
        user2 = self.create_user(username='Paula', email='paula@gmail.com')
        self.expense2 = self.create_expense(user2)

        self.expense_data = {
            'description': 'A new TV for my bedroom',
            'date': datetime.now(tz=pytz.UTC).strftime('%Y-%m-%d'),
            'time': datetime.now(tz=pytz.UTC).strftime('%I:%M %p'),
            'amount': '700',
            'comment': 'my old one is broken',
        }

    def test_delete_expense(self):
        """ Good delete request should return 204 no content status code """
        resp = self.client.delete(r('core:expense_detail',
                                    kwargs={'pk': self.expense1.id}),
                                  **self.auth_headers)
        self.assertEquals(204, resp.status_code)
        with self.assertRaises(Expense.DoesNotExist):
            Expense.objects.get(pk=self.expense1.id)

    def test_delete_different_user(self):
        """ Deleting an expense from a different user should return status \
            code 403 forbidden """
        resp = self.client.delete(r('core:expense_detail',
                                    kwargs={'pk': self.expense2.id}),
                                  **self.auth_headers)
        self.assertEquals(403, resp.status_code)

    def test_delete_nonexistent(self):
        """ Deleting an expense already deleted should return status code 404 \
            not found """

        resp = self.client.delete(r('core:expense_detail',
                                    kwargs={'pk': self.expense1.id}),
                                  **self.auth_headers)
        resp = self.client.delete(r('core:expense_detail',
                                    kwargs={'pk': self.expense1.id}),
                                  **self.auth_headers)
        self.assertEquals(404, resp.status_code)
