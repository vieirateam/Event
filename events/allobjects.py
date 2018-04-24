from events.models import Event, Talk
from speakers.models import Speaker

def getAllObjects():
    events = Event.objects.all().order_by('eventName')
    talks = Talk.objects.filter(talkApproved=True).order_by('talkName')
    speakers = Speaker.objects.filter(speakerApproved=True).order_by('speakerName')
    objectsList = [events,talks,speakers]
    return objectsList
