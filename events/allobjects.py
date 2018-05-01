from events.models import Event, Talk, Speaker

def getAllObjects():
    events = Event.objects.all().order_by('startDate')
    talks = Talk.objects.filter(approved=True).order_by('date')
    speakers = Speaker.objects.filter(approved=True).order_by('name')
    objectsList = [events,talks,speakers]
    return objectsList
