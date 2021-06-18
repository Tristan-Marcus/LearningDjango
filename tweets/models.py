import random
from django.conf import settings
from django.db import models

# Create your models here.

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    #* id is created automatically when this (or any) model is saved to the DB
    #* models.AutoField(primary_key=True) is how you would access it
    # id = models.AutoField(primary_key=true)

    #* Giving a user a Foreign Key allowed for them to own more than one tweet
    #* this line below means that one tweet can only have one user though
    #* on_delete=models.CASCADE deletes all tweets associated with the user if the user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #* Many to Many = 1 tweet can have many users, many users can have many tweets.
    #* likes references the class above, TweetLike table, through=TweetLike
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)

    #* This is the text field that will be stored in the DB called content
    content = models.TextField(blank=True, null=True)


    #* This is for uploading a file to the DB, however what is stored
    #* Data stored in DB will be the image path 
    #* blank means Not required in Django
    #* null means not required in the DB
    # image = models.FileField(upload_to='images/' blank=True, null=True)

    #* This adds a timestamp field to the table
    timestamp = models.DateTimeField(auto_now_add=True)

    #* Below changes the meta data
    #* adds decending ordering based on id
    class Meta:
        ordering = ['-id']


    # This serializes the Tweet so that it can return its content as JSON data
    # This method is called in the views as  obj.serialize()
    # It will then return that obj id, content, and likes in a json response
    def serialize(self):
        return{
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 93)
        }