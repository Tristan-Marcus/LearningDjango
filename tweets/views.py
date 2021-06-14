from django.http import HttpResponse
from django.http.response import Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet

# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def tweet_list_view(request, *args, **kwargs):
    '''
    REST API VIEW
    Consumed by JavaScript by returning JSON data
    '''

    # QuerySet is a list of objects, in this case its all objects in a Tweet
    querySet = Tweet.objects.all()

    # map the data from querySet to the dictionary in tweets_list
    tweets_list = [{"id": x.id, "content": x.content} for x in querySet]

    data = {
        "TWEETS :)": tweets_list
    }

    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    '''
    REST API VIEW
    Consumed by JavaScript by returning JSON data
    '''

    data = {
        "id": tweet_id,
    }

    status = 200

    try:
        obj = Tweet.objects.get(id=tweet_id)

        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404
    
    
    return JsonResponse(data, status=status)
