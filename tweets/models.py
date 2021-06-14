from django.db import models

# Create your models here.


class Tweet(models.Model):
    #* id is created automatically when this (or any) model is saved to the DB
    #* models.AutoField(primary_key=True) is how you would access it
    # id = models.AutoField(primary_key=true)
    

    #* This is the text field that will be stored in the DB called content
    content = models.TextField(blank=True, null=True)


    #* This is for uploading a file to the DB, however what is stored
    #* Data stored in DB will be the image path 
    #* blank means Not required in Django
    #* null means not required in the DB
    # image = models.FileField(upload_to='images/' blank=True, null=True)