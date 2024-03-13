from django.test import TestCase
from django.utils import timezone
from login.models import OsmUser
from core.models import Dataset, AOI, Model, Training, Feedback, FeedbackAOI, FeedbackLabel


class DatasetModelTest(TestCase):
    """Test case for the Dataset model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.user = OsmUser.objects.create_user(username='test_user', email='test@example.com', password='testpass')
        cls.dataset = Dataset.objects.create(name='Test Dataset', created_by=cls.user)

    def test_name_max_length(self):
        """Test maximum length of the dataset name."""
        max_length = self.dataset._meta.get_field('name').max_length
        self.assertLessEqual(len(self.dataset.name), max_length)

    def test_status_choices(self):
        """Test choices for dataset status."""
        self.assertIn(self.dataset.status, [choice[0] for choice in Dataset.DatasetStatus.choices])


class AOIModelTest(TestCase):
    """Test case for the AOI model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.user = OsmUser.objects.create_user(username='test_user', email='test@example.com', password='testpass')
        cls.dataset = Dataset.objects.create(name='Test Dataset', created_by=cls.user)
        cls.aoi = AOI.objects.create(dataset=cls.dataset)

    def test_label_status_choices(self):
        """Test choices for label status of AOI."""
        self.assertIn(self.aoi.label_status, [choice[0] for choice in AOI.DownloadStatus.choices])


class ModelModelTest(TestCase):
    """Test case for the Model model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.user = OsmUser.objects.create_user(username='test_user', email='test@example.com', password='testpass')
        cls.dataset = Dataset.objects.create(name='Test Dataset', created_by=cls.user)
        cls.model = Model.objects.create(name='Test Model', dataset=cls.dataset, created_by=cls.user)

    def test_status_choices(self):
        """Test choices for model status."""
        self.assertIn(self.model.status, [choice[0] for choice in Model.ModelStatus.choices])


class TrainingModelTest(TestCase):
    """Test case for the Training model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.user = OsmUser.objects.create_user(username='test_user', email='test@example.com', password='testpass')
        cls.dataset = Dataset.objects.create(name='Test Dataset', created_by=cls.user)
        cls.model = Model.objects.create(name='Test Model', dataset=cls.dataset, created_by=cls.user)
        cls.training = Training.objects.create(model=cls.model, created_by=cls.user, epochs=1, batch_size=1)

    def test_source_imagery_blank(self):
        """Test blank source imagery for training."""
        self.assertEqual(self.training.source_imagery, '')

    def test_status_choices(self):
        """Test choices for training status."""
        self.assertIn(self.training.status, [choice[0] for choice in Training.STATUS_CHOICES])

    def test_zoom_level_max_size(self):
        """Test maximum size of zoom levels."""
        max_size = Training._meta.get_field('zoom_level').size
        self.assertLessEqual(len(self.training.zoom_level), max_size)


class FeedbackModelTest(TestCase):
    """Test case for the Feedback model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.user = OsmUser.objects.create_user(username='test_user', email='test@example.com', password='testpass')
        cls.dataset = Dataset.objects.create(name='Test Dataset', created_by=cls.user)
        cls.model = Model.objects.create(name='Test Model', dataset=cls.dataset, created_by=cls.user)
        cls.training = Training.objects.create(model=cls.model, created_by=cls.user, epochs=1, batch_size=1)
        cls.feedback = Feedback.objects.create(training=cls.training, user=cls.user, feedback_type='TP')

    def test_zoom_level_min_value(self):
        """Test minimum value of zoom level."""
        self.assertGreaterEqual(self.feedback.zoom_level, 18)

    def test_zoom_level_max_value(self):
        """Test maximum value of zoom level."""
        self.assertLessEqual(self.feedback.zoom_level, 23)

    def test_feedback_type_choices(self):
        """Test choices for feedback type."""
        self.assertIn(self.feedback.feedback_type, [choice[0] for choice in Feedback.FEEDBACK_TYPE])


class FeedbackAOIModelTest(TestCase):
    """Test case for the FeedbackAOI model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.user = OsmUser.objects.create_user(username='test_user', email='test@example.com', password='testpass')
        cls.dataset = Dataset.objects.create(name='Test Dataset', created_by=cls.user)
        cls.model = Model.objects.create(name='Test Model', dataset=cls.dataset, created_by=cls.user)
        cls.training = Training.objects.create(model=cls.model, created_by=cls.user, epochs=1, batch_size=1)
        cls.feedback_aoi = FeedbackAOI.objects.create(training=cls.training, user=cls.user)

    def test_label_status_choices(self):
        """Test choices for label status of FeedbackAOI."""
        self.assertIn(self.feedback_aoi.label_status, [choice[0] for choice in FeedbackAOI.DownloadStatus.choices])


class FeedbackLabelModelTest(TestCase):
    """Test case for the FeedbackLabel model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.user = OsmUser.objects.create_user(username='test_user', email='test@example.com', password='testpass')
        cls.dataset = Dataset.objects.create(name='Test Dataset', created_by=cls.user)
        cls.model = Model.objects.create(name='Test Model', dataset=cls.dataset, created_by=cls.user)
        cls.training = Training.objects.create(model=cls.model, created_by=cls.user, epochs=1, batch_size=1)
        cls.feedback_aoi = FeedbackAOI.objects.create(training=cls.training, user=cls.user)
        cls.feedback_label = FeedbackLabel.objects.create(feedback_aoi=cls.feedback_aoi)

    def test_osm_id_blank(self):
        """Test blank OSM ID for FeedbackLabel."""
        self.assertIsNone(self.feedback_label.osm_id)
