from django.shortcuts import render,redirect
from  django.http import HttpResponse,Http404,JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated


from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer,TweetActionSerializer,TweetCreateSerializer
import random

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.

def home_view(request,*args,**kwargs):
    print(request.user or None)
    context={}
    return render(request,'pages/home.html',context)

@api_view(['POST',])
# @authentication_classes([SessionAuthentication,MyCustomAuth])
@permission_classes([IsAuthenticated])
def tweet_create_view(request,*args,**kwargs):
    data = request.POST or None 
    serializer = TweetCreateSerializer(data = data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data,status=201)
    return Response({},status=400)

@api_view(['GET',])
def tweet_detail_view(request,tweet_id,*args,**kwargs):
    qs = Tweet.objects.get(id=tweet_id)
    if not qs:
         return Response({},status=404)
    # obj = qs.first()
    serializer = TweetSerializer(qs)
    return Response(serializer.data,status=200)

@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request,tweet_id,*args,**kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    qs = qs.filter(user=request.user)
    if not qs:
         return Response({},status=404)
    # obj = qs.first()
    qs=qs.filter(user=request.user)
    if not qs:
         return Response({'message':'You can not delete this tweet '},status=404)
    qs.delete()
    return Response({'message':'tweet removed'},status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request,*args,**kwargs):
    '''
    id required 
    Action option are : like,unlike,  retweet 
    '''
    
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        print('##################3 insed the retweet',request.data)
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')

        qs = Tweet.objects.filter(id=tweet_id)
        qs = qs.filter(user=request.user)
        obj = qs.first()
        
        if not qs.exists:
            return Response({},status=404)
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data,status=200)

        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data,status=200)

        elif action == 'retweet':
            newchild_obj = Tweet.objects.create(user=request.user,parent=obj,content=content)
            serializer = TweetSerializer(newchild_obj)
            return Response(serializer.data,status=201)
    return Response({'message':'tweet removed'},status=200)

@api_view(['GET',])
def tweet_list_view(request,*args,**kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs,many=True)
    return Response(serializer.data)



def tweet_create_pure_django(request,*args,**kwargs):
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

def tweet_list_view_pure_django(request,*args,**kwargs):
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

def tweet_detail_view_pure_django(request,tweet_id,*args,**kwargs):

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