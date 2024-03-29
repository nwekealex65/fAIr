import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from unittest.mock import patch, MagicMock
from .models import OsmUser
from .authentication import OsmAuthentication


class OsmAuthenticationTestCase(TestCase):
    def setUp(self):
        """
        Set up the test environment by initializing necessary variables and objects.
        """
        self.client = Client()
        self.auth = OsmAuthentication()
        self.test_user_data = {
            "id": 123,
            "username": "test_user",
            "img_url": "https://example.com/test_user.jpg"
        }
        self.access_token = "test_access_token"

    @patch('osm_login_python.core.Auth')
    def test_authenticate_success(self, mocked_auth):
        """
        Test successful authentication with valid access token.
        """
        # Mocking Auth class and its methods
        mocked_auth_instance = mocked_auth.return_value
        mocked_auth_instance.deserialize_access_token.return_value = self.test_user_data
        request = MagicMock()
        request.headers = {"access-token": self.access_token}
        
        # Mocking settings
        with self.settings(
            OSM_URL="test_osm_url",
            OSM_CLIENT_ID="test_client_id",
            OSM_CLIENT_SECRET="test_client_secret",
            OSM_SECRET_KEY="test_secret_key",
            OSM_LOGIN_REDIRECT_URI="test_login_redirect_uri",
            OSM_SCOPE="test_scope"
        ):
            user, _ = self.auth.authenticate(request)
        
        # Check if user object is correctly populated
        self.assertEqual(user.osm_id, self.test_user_data["id"])
        self.assertEqual(user.username, self.test_user_data["username"])
        self.assertEqual(user.img_url, self.test_user_data["img_url"])

    @patch('osm_login_python.core.Auth')
    def test_authenticate_failure(self, mocked_auth):
        """
        Test authentication failure when an exception occurs during authentication.
        """
        # Mocking Auth class and causing it to raise an exception
        mocked_auth_instance = mocked_auth.return_value
        mocked_auth_instance.deserialize_access_token.side_effect = Exception("Test Exception")
        request = MagicMock()
        request.headers = {"access-token": self.access_token}

        # Mocking settings
        with self.settings(
            OSM_URL="test_osm_url",
            OSM_CLIENT_ID="test_client_id",
            OSM_CLIENT_SECRET="test_client_secret",
            OSM_SECRET_KEY="test_secret_key",
            OSM_LOGIN_REDIRECT_URI="test_login_redirect_uri",
            OSM_SCOPE="test_scope"
        ):
            # Ensure the correct exception is raised
            with self.assertRaisesRegex(Exception, "Osm Authentication Failed"):
                self.auth.authenticate(request)

    def test_authenticate_no_access_token(self):
        """
        Test case for authentication when no access token is provided.
        """
        request = MagicMock()
        request.headers = {}

        # Ensure the correct exception is raised
        with self.assertRaisesRegex(
            AuthenticationFailed, "Access token not supplied"  # Updated exception class
        ):
            self.auth.authenticate(request)

    def test_authenticate_user_not_exist(self):
        """
        Test case for authentication when the user does not exist in the database.
        """
        request = MagicMock()
        request.headers = {"access-token": self.access_token}
        
        # Mocking settings
        with self.settings(
            OSM_URL="test_osm_url",
            OSM_CLIENT_ID="test_client_id",
            OSM_CLIENT_SECRET="test_client_secret",
            OSM_SECRET_KEY="test_secret_key",
            OSM_LOGIN_REDIRECT_URI="test_login_redirect_uri",
            OSM_SCOPE="test_scope"
        ):
            # Mocking database query to simulate user not existing
            with patch.object(OsmUser.objects, 'get') as mocked_get:
                mocked_get.side_effect = OsmUser.DoesNotExist
                user, _ = self.auth.authenticate(request)
        
        # Ensure no user is returned and database query is not executed
        self.assertIsNone(user)
        mocked_get.assert_not_called()
