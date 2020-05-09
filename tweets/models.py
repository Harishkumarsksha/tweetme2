from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.


class TweetLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    parent = models.ForeignKey("self",null=True,on_delete=models.SET_NULL,)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(null=True,blank=True)
    likes = models.ManyToManyField(User,blank=True,related_name='tweet_user',through='TweetLike')
    image =  models.FileField(upload_to='images/',null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.parent != None

    def serialize(self):
        return  {"id":self.id,"content":self.content,"Likes":random.randint(0,101)}
    def __str__(self):
        return self.content