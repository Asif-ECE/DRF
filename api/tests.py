# from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


class TestClass(APITestCase):
    def setUp(self):
        signup_url = '/api/signup/'

        signup_data = {
            "email": "test@test.com",
            "username": "test",
            "password": "testPassword1234"
        }

        response = self.client.post(
            signup_url, data=signup_data, format="json")

        login_url = '/api/token/'

        login_data = {
            "email": "test@test.com",
            "password": "testPassword1234"
        }

        response = self.client.post(login_url, data=login_data, format="json")

        self.jwt_access = response.data["access"]
        self.jwt_refresh = response.data["refresh"]

    def test_category_endpoint(self):
        url = '/api/categories/'

        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.jwt_access}")

        self.assertEqual(response.status_code, 200)

    def test_category_post(self):
        url = '/api/categories/'

        data = {
            "name": "Electronics"
        }

        response = self.client.post(
            url, data=data, format="json", HTTP_AUTHORIZATION=f"Bearer {self.jwt_access}")

        expected_data = {
            "id": 1,
            "name": "Electronics",
            "itemsAvailable": 0,
            "on_sale": "We have 0 items on sale."
        }

        self.assertEqual(response.data, expected_data)
