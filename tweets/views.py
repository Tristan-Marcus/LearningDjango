from tweetme2.settings import ALLOWED_HOSTS
from django.conf import settings
from django.http import HttpResponse
from django.http.response import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet


# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):

    """
    Up until now, this view has been vanilla Django implementation

    HOWEVER, we can make this less complex and BETTER using the Django REST framework

    It will turn this view into a REST API CRUD (Create, Read, Update, Delete) view.
    """

    #* Store the user from the request data
    user = request.user

    # handles authentication for a json request and a regular http request.
    # This will execute if a tweet creation is attempted without a user attached to it.
    if not request.user.is_authenticated:
        # user = None is to make sure the tweet without an authenitcated user will show as None
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)

    # the TweetForm class can be initialized with data
    # in this case, request.POST would be the post data that the form collected
    # OR
    # it could be initialized with no data, hense 'None'
    form = TweetForm(request.POST or None)

    # This will return the next url when the form is POSTed.
    # This can be used to redirect the user.
    # This gets the HTML element with the name "next" and returns its value which is "/"
    next_url = request.POST.get("next") or None
    
    # if the form is valid, it saves the form
    # else, the page will render an invalid form
    if form.is_valid():
        obj = form.save(commit=False)

        #* This is added to associate the tweet obj with a user upon form submission
        obj.user = user

        # save the form to the database
        obj.save()

        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items

        # this will redirect the user to next_url which is "/" if the form was submitted with a POST
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)

        # reinitialize a new blank form
        # This is then passed to the component in render
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    return render(request, "components/form.html", context={"form": form})


def tweet_list_view(request, *args, **kwargs):
    '''
    REST API VIEW
    Consumed by JavaScript by returning JSON data
    '''

    # QuerySet is a list of objects, in this case its all objects in a Tweet
    querySet = Tweet.objects.all()

    # map the data from querySet to the dictionary in tweets_list
    tweets_list = [x.serialize() for x in querySet]

    data = {
        "isUser": False,
        "response": tweets_list
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
