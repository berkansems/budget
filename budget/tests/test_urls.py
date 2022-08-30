from django.test import SimpleTestCase
from django.urls import reverse, resolve
from budget.views import project_list, project_detail, ProjectCreateView

class TestUrls(SimpleTestCase):
    def test_list_urls_resolved(self):
        url = reverse('list')
        self.assertEqual(resolve(url).func, project_list)


    def test_add_url(self):
        url = reverse('add')
        self.assertEqual(resolve(url).func.view_class, ProjectCreateView)

    def test_detail_url(self):
        url = reverse('detail', args=['some-slug'])
        self.assertEqual(resolve(url).func, project_detail)