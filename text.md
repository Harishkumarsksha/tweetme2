from django.shortcuts import render
from  django.http import HttpResponse,Http404,JsonResponse
from .models import Tweet



# Create your views here.

def home_view(request,*args,**kwargs):
    return HttpResponse('<h1> Welcome to The Tweets Home Pages</h1>')

def tweet_detail_view(request,tweet_id,*args,**kwargs):

    """ Implementing The REST API
        consume by the JS ios/Android Java
    
    """
    data = {
        "id":tweet_id,
    }
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"]=obj.content
        return JsonResponse(data,status=200)
        # string = '<h1> Requested Tweet Id :'+tweet_id+'requested tweet'+obj.content+'</h1>'
        # return HttpResponse(string)
    except:
        data["content"]="Content Not found"
        # raise Http404
        return JsonResponse(data,status=404)





from django.shortcuts import render,redirect
from  django.http import HttpResponse,Http404,JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings
from .models import Tweet
from .forms import TweetForm
import random

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.

def home_view(request,*args,**kwargs):
    print(request.user or None)
    context={}
    return render(request,'pages/home.html',context)

def tweet_create(request,*args,**kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({},status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user 
        obj.save()
        
        if request.is_ajax():
            return JsonResponse(obj.serialize(),status=201) # resource is created 
        if next_url !=None and is_safe_url(next_url,ALLOWED_HOSTS):
            return redirect(next_url)
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors,status=400)
    form = TweetForm()
    context={'form':form}
    return render(request,'components/form.html',context)

def tweet_list_view(request,*args,**kwargs):
    """ Implementing The REST API
        consume by the JS ios/Android Java
    
    """
    qs = Tweet.objects.all()
    tweet_list = [x.serialize() for x in qs ]
    data = {
        "isUser":False,
        
        "response":tweet_list
    }
    return JsonResponse(data)

def tweet_detail_view(request,tweet_id,*args,**kwargs):

    """ Implementing The REST API
        consume by the JS ios/Android Java
    
    """
    data = {
        "id":tweet_id,
    }
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"]=obj.content
        return JsonResponse(data,status=200)
        # string = '<h1> Requested Tweet Id :'+tweet_id+'requested tweet'+obj.content+'</h1>'
        # return HttpResponse(string)
    except:
        data["content"]="Content Not found"
        # raise Http404
        return JsonResponse(data,status=404)