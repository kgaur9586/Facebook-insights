from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from insights.models import Page

class PageAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_page(self):
        response = self.client.get('/api/pages/?username=boat.lifestyle')
        self.assertEqual(response.status_code, 200)