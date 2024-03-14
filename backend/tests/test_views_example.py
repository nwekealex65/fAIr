from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Dataset, Training

class DatasetViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dataset = Dataset.objects.create(name="Test Dataset")
        self.training = Training.objects.create(name="Test Training")

    def test_list_datasets(self):
        """
        Test the list functionality of datasets.
        """
        url = reverse('dataset-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one dataset is created in setup

    def test_retrieve_dataset(self):
        """
        Test the retrieval of a single dataset.
        """
        url = reverse('dataset-detail', kwargs={'pk': self.dataset.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.dataset.name)

class TrainingViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.training = Training.objects.create(name="Test Training")

    def test_list_trainings(self):
        """
        Test the list functionality of trainings.
        """
        url = reverse('training-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one training is created in setup

    def test_retrieve_training(self):
        """
        Test the retrieval of a single training.
        """
        url = reverse('training-detail', kwargs={'pk': self.training.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.training.name)
