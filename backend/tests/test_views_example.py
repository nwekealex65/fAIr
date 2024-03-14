from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Dataset

class DatasetViewsTestCase(TestCase):
    def setUp(self):
        """
        Method called before each test method to set up initial data.
        """
        self.client = APIClient()
        self.dataset = Dataset.objects.create(name="Test Dataset")

    def test_list_datasets(self):
        """
        Test case to verify the API endpoint for listing datasets.
        """
        url = reverse('dataset-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one dataset is created in setup

    def test_retrieve_dataset(self):
        """
        Test case to verify the API endpoint for retrieving a specific dataset.
        """
        url = reverse('dataset-detail', kwargs={'pk': self.dataset.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.dataset.name)

    def test_create_dataset(self):
        """
        Test case to verify the creation of a new dataset via the API endpoint.
        """
        url = reverse('dataset-list')
        data = {'name': 'New Dataset'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dataset.objects.count(), 2)  # Assuming only one dataset is created in setup

    def test_update_dataset(self):
        """
        Test case to verify the update of an existing dataset via the API endpoint.
        """
        url = reverse('dataset-detail', kwargs={'pk': self.dataset.pk})
        data = {'name': 'Updated Dataset'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dataset.refresh_from_db()
        self.assertEqual(self.dataset.name, 'Updated Dataset')

    def test_delete_dataset(self):
        """
        Test case to verify the deletion of an existing dataset via the API endpoint.
        """
        url = reverse('dataset-detail', kwargs={'pk': self.dataset.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dataset.objects.count(), 0)
