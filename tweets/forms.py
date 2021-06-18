from django.conf import settings
from django import forms

from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

class TweetForm(forms.ModelForm):
    # Meta class just defines our tweet form
    class Meta:
        model = Tweet
        fields = ['content']

    # Clean content is just making sure that content is less than the max tweet length
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        
        return content