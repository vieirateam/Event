from django import forms
from .models import Event, Talk, Speaker

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'desc', 'startDate', 'finishDate', 'image', 'latitude', 'longitude' )

class SpeakerForm(forms.ModelForm):

    class Meta:
        model = Speaker
        fields = ('name', 'email', 'formation', 'bio', 'image', )

class TalkForm(forms.ModelForm):

	class Meta:
		model = Talk
		fields = ('event', 'speakers', 'name', 'category', 'desc', 'maxPeople', 'date', 'startTime', 'finishTime', 'location', 'approved', )

class ContactForm(forms.Form):
	email = forms.EmailField(required=True)
	subject = forms.CharField(required=True)
	message = forms.CharField(widget=forms.Textarea)
