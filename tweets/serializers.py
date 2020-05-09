from rest_framework import serializers
from django.conf import settings
from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTIONS_OPTIONS = settings.TWEET_ACTIONS_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(required=False,allow_blank=True)
    def validated_action(self,value):
        value = value.lower().strip()
        if not value in TWEET_ACTIONS_OPTIONS:
            raise serializers.ValidationError("This is not valid action for tweet")
        else:
            return value
            
class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id','content','likes']

    def validated_content(self,value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError('Tweet is  too long')
        else:
            return value

    def get_likes(self,obj):
        return obj.likes.count()

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    #content = serializers.SerializerMethodField(read_only=True)
    # is_retweet = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id','content','likes','is_retweet','parent']

    def get_likes(self,obj):
        return obj.likes.count()

    # def get_content(self,obj):
    #     content = obj.content 
    #     if obj.is_retweet:
    #         content = obj.parent.content
    #     return content


