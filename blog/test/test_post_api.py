import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoProject7.settings'
django.setup()


import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import datetime
from accounts.models import User
# api test

@pytest.mark.django_db
class TestPostApi:
    client = APIClient()
    def test_get_post_response_200_Status(self):

        url = reverse('blog:api-v1:post-list')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_Status(self):
        url = reverse('blog:api-v1:post-list')
        data = {'title': 'test title', 'context': 'test', 'status': True, 'published_date': datetime.now()}
        response = self.client.post(url, data)
        assert response.status_code == 401

    def test_create_post_response_201_Status(self):
        url = reverse('blog:api-v1:post-list')
        data = {'title': 'test title', 'context': 'test', 'status': True, 'published_date': datetime.now()}
        user = User.objects.create_user(email='test@test.com', password='test1380')
        self.client.force_authenticate(user =user)

        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_create_post_invalid_data_response_400_Status(self):
        url = reverse('blog:api-v1:post-list')
        data = {'title': 'test title'}
        user = User.objects.create_user(email='test@test.com', password='test1380')
        self.client.force_authenticate(user =user)

        response = self.client.post(url, data)
        assert response.status_code == 400