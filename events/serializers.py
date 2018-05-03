from rest_framework import serializers
from .models import Event, Talk, Speaker

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'desc', 'startDate', 'finishDate', 'image', 'latitude', 'longitude' )

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ('name', 'email', 'formation', 'bio', 'image', )

class TalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talk
        fields = ('event', 'speakers', 'name', 'category', 'desc', 'maxPeople', 'date', 'startTime', 'finishTime', 'location', )