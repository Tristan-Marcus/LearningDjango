from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Tweet

# Create your tests here.
User = get_user_model

class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='abc', password='somepassword')
        Tweet.objects.create(content="my 1 tweet", user=self.user)
        Tweet.objects.create(content="my 2 tweet", user=self.user)
        Tweet.objects.create(content="my 3 tweet", user=self.user)


    #* Vanilla Django Testing
    def test_tweet_created(self):
       tweet_obj = Tweet.objects.create(content="my 4 tweet", user=self.user)
       self.assertEqual(tweet_obj.id, 4)
       self.assertEqual(tweet_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        
        return client

    #* Django REST Framework Testing
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("api/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
