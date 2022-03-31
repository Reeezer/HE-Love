from django import forms

class ImageForm(forms.Form):
    image = forms.ImageField()
    name = forms.CharField()
    
class JoinEventForm(forms.Form):
    event_id = forms.IntegerField()