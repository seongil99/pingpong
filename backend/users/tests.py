from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.management import call_command

from .models import User


class MyProfileTestCase(APITestCase):
    def setUp(self):
        call_command('migrate', verbosity=0)
        self.user = User.objects.create_user(
            email="seonyoon@student.42seoul.kr",
            password="1234",
            username="seonyoon",
            is_verified=False,
            avatar=None,
        )
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('my-profile')

    def test_my_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['is_verified'], self.user.is_verified)

    def test_update_my_profile(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        avatar = SimpleUploadedFile(
            name="avatar.jpg",
            content=b'\x47\x49\x46\x38\x37\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x0A\x00\x01\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3B',
            content_type="image/jpeg"
        )
        data = {
            'username': 'seonyoon2',
            'is_verified': True,
            'avatar': avatar,
        }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['is_verified'], data['is_verified'])
        self.assertIsNotNone(response.data['avatar'])
