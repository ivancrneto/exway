from django.test import TestCase
from django.core.urlresolvers import reverse as r


class ExpensesAPITest(TestCase):
    def setUp(self):
        pass

    def test_get_expenses_no_auth(self):
        resp = self.client.get(r('core:expenses'))
        self.assertEqual(403, resp.status_code)

