from django import forms
from .models import Speaker

class SpeakerForm(forms.ModelForm):

    class Meta:
        model = Speaker
        fields = ('speakerName', 'speakerEmail', 'speakerFormation', 'speakerBio', 'speakerImage')