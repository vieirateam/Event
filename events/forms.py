from django import forms
from .models import Event, Talk

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('eventName', 'eventDesc', 'eventStartDate', 'eventFinishDate', 'eventImage', )

class TalkForm(forms.ModelForm):

	class Meta:
		model = Talk
		fields = ('eventId', 'speakerId', 'talkName', 'talkType', 'talkDesc', 'talkMaxPeople', 'talkDate', 'talkStartTime', 'talkFinishTime', 'talkLocation', 'talkApproved', )

class ContactForm(forms.Form):
	email = forms.EmailField(required=True)
	subject = forms.CharField(required=True)
	message = forms.CharField(widget=forms.Textarea)