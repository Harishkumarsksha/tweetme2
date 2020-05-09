from django.test import TestCase
from django.contrib.auth.models import User 


from rest_framework.test import APIClient
# Create your tests here.
from .models import Tweet

class TweetTestCases(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='mohan',password='mohan123')

    def test_user_created(self):
        # user = User.objects.create(username='mohan',password='mohan123')
        self.assertEqual(self.user.username,'mohan')

    def test_tweet_created(self):

        tweet_obj= Tweet.objects.create(content="my first Content",user=self.user)
        self.assertEqual(tweet_obj.id,1)
        self.assertEqual(tweet_obj.user,self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username,password='mohan123')
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("api/tweets/")
        #self.assertEqual(response.status_code,200)
        #self.assertEqual(len(response.json()),1)
        print(response)

    def test_action_like(self):
        client = self.get_client()
        response = client.get("api/tweets/action/",{"id":1,"action":"like"})
        #like_count = response.json().get('like')
        #self.assertEqual(like_count,1)
        #self.assertEqual(response.status_code,200)
        #self.assertEqual(len(response),200)
        print(response)

     def test_action_unlike(self):
        client = self.get_client()
        response = client.get("api/tweets/action/",{"id":1,"action":"like"})
        #self.assertEqual(response.status_code,200)
         response = client.get("api/tweets/action/",{"id":1,"action":"unlike"})
        #self.assertEqual(response.status_code,200)

        #like_count = response.json().get('like')
        #self.assertEqual(like_count,0)
        
        #self.assertEqual(len(response),200)
        print(response)


        def test_action_retweet(self):
        client = self.get_client()
        response = client.get("api/tweets/action/",{"id":1,"action":"retweet"})
        #self.assertEqual(response.status_code,201)
        data = response.json()
        new_tweet_id = data.get('id')
        self.assertNotEqual(1,new_tweet_id)