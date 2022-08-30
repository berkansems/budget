from django.test import SimpleTestCase

from budget.forms import ExpenseForm


class TestForms(SimpleTestCase):

    def test_expense_form_is_valid_data(self):
        form = ExpenseForm(data={
            'title' : 'test title',
            'amount' : 30,
            'category' : 'cat1,cat2'
        })
        self.assertTrue(form.is_valid())

    def test_unvalid_expense_form_data(self):
        form = ExpenseForm(data={
            'title': 'test title',
            'amount': 'unv',
            'category': 'cat1,cat2'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)