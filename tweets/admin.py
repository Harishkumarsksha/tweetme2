from django.contrib import admin

# Register your models here.
from .models import Tweet,TweetLike


class TweetLikeAdmin(admin.TabularInline):
        model = TweetLike
            

class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]
    list_display = ('id','__str__','content')
    search_fields = ['content','user_username','user_email']
    class Meta:
        model = Tweet
admin.site.register(Tweet,TweetAdmin)
