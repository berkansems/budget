from django.test import TestCase, Client
from django.urls import resolve, reverse
from budget.models import Project, Expense, Category
import json

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['project1'])
        self.project1 = Project.objects.create(
            name= 'project1',
            budget= 100
        )

    def test_project_list_get(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')

    def test_project_detail_get(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')

    def test_project_detail_post_add_expense(self):
        Category.objects.create(
            project = self.project1,
            name='cat1'
        )
        response = self.client.post(self.detail_url,{
            'title':'expense1',
            'amount':2,
            'category':'cat1'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project1.expenses.first().title, 'expense1')

    def test_project_detail_post_delete_without_expense_creation(self):
        response = self.client.post(self.detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project1.expenses.count(), 0)

    def test_project_detail_expense_delete(self):
        category = Category.objects.create(
            project=self.project1,
            name='cat1'
        )
        Expense.objects.create(
            project=self.project1,
            title = 'expense_test',
            amount = 44,
            category = category
        )
        response = self.client.delete(self.detail_url, json.dumps({'id':1}))
        self.assertEqual(response.status_code, 204)

    def test_project_detail_expense_delete_no_id(self):
        category = Category.objects.create(
            project=self.project1,
            name='cat1'
        )
        Expense.objects.create(
            project=self.project1,
            title = 'expense_test',
            amount = 44,
            category = category
        )
        response = self.client.delete(self.detail_url, json.dumps({'id':2}))
        self.assertEqual(response.status_code, 404)

    def test_project_create_post(self):
        url = reverse('add')
        response = self.client.post(url, {
            'name': 'pro_test',
            'budget': 10,
            'categoriesString': 'cat1,cat2'
        })
        project2 = Project.objects.get(id=2)
        category1 = Category.objects.get(id=1)
        category2 = Category.objects.get(id=2)
        self.assertEqual(project2.name, 'pro_test')
        self.assertEqual(category1.project.name, 'pro_test')
        self.assertEqual(category1.name, 'cat1')
        self.assertEqual(category2.project.name, 'pro_test')
        self.assertEqual(category2.name, 'cat2')
