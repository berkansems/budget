from unittest import TestCase

from budget.models import Project, Category, Expense


class TestModel(TestCase):
    def setUp(self) -> None:
        self.project1 = Project.objects.create(
            name = 'project 1',
            budget = 100
        )
    def test_project_assign_slug_in_creation(self):
        self.assertEqual(self.project1.slug, 'project-1')
        cat1 = Category.objects.create(
            name = 'category1',
            project = self.project1
        )
        expense1 = Expense.objects.create(
            project=self.project1,
            category=cat1,
            amount= 20,
            title= 'ex1'
        )
        expense2 = Expense.objects.create(
            project=self.project1,
            category=cat1,
            amount=20,
            title='ex2'
        )
        self.assertEqual(self.project1.budget_left,
                         self.project1.budget - (expense1.amount + expense2.amount))
        self.assertEqual(self.project1.total_transactions, self.project1.expenses.count())
