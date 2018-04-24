from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from .models import Event, Talk
from speakers.models import Speaker
from . import allobjects
from .forms import EventForm, TalkForm, ContactForm

def home(request):
    if request.method == 'GET':
        objectsList = allobjects.getAllObjects()
        nextEvents = Event.objects.all().order_by('eventStartDate')[:4]
        emailForm = ContactForm()
    else:
        emailForm = ContactForm(request.POST)
        if emailForm.is_valid():
            email = emailForm.cleaned_data['email']
            subject = emailForm.cleaned_data['subject']
            message = emailForm.cleaned_data['message']
            try:
                send_mail(subject, message, email, ['vieirateam.contact@gmail.com'])
            except BadHeaderError:
                return HttpResponse("Erro =/")
        return redirect('home')
    return render(request, 'index.html', {'form': emailForm, 'list': objectsList, 'nextEvents': nextEvents}) 

def pendencyList(request):
    if request.user.is_superuser:
        talksNotApproved = Talk.objects.filter(talkApproved=False)
        speakersNotApproved = Speaker.objects.filter(speakerApproved=False)
        return render(request, 'pendencyList.html', {'talks': talksNotApproved, 'speakers': speakersNotApproved})
    return redirect('home')

def eventList(request):
    objectsList = allobjects.getAllObjects()
    events = objectsList[0]
    return render(request, 'events/eventList.html', {'events': events, 'list': objectsList})

def eventDetail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    objectsList = allobjects.getAllObjects()
    return render(request, 'events/eventDetail.html', {'event': event, 'list': objectsList})

@login_required
@permission_required('is_superuser', 'eventList')
def eventNew(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('eventDetail', pk=event.pk)
    else:
        form = EventForm()
        objectsList = allobjects.getAllObjects()
    return render(request, 'events/eventEdit.html', {'form': form, 'list': objectsList})

@login_required
@permission_required('is_superuser', 'eventList')
def eventEdit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    objectsList = allobjects.getAllObjects()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('eventDetail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/eventEdit.html', {'form': form, 'new': "Editar", 'list': objectsList})

@login_required
@permission_required('is_superuser', 'eventList')
def eventRemove(request, pk):
    if request.user.is_superuser:
        event = get_object_or_404(Event, pk=pk)
        event.delete()
        return redirect('eventList')

def talkDetail(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    objectsList = allobjects.getAllObjects()
    if talk.talkApproved or request.user.is_authenticated:
        userIsParticipant = False
        
        if hasattr(request.user, 'speaker'):
            userIsParticipant = talk.speakerId.filter(id=request.user.speaker.id).exists()
        
        return render(request, 'talks/talkDetail.html', {'talk': talk, 'userIsParticipant': userIsParticipant, 'list': objectsList})
    return redirect('eventDetail', pk=talk.eventId.pk)

@login_required
def talkNew(request):
    events = Event.objects.all()
    if request.method == "POST":
        form = TalkForm(request.POST)
        if form.is_valid():
            talk = form.save(commit=False)
            talk.save()
            form.save_m2m()
            return redirect('talkDetail', pk=talk.pk)
    else:
        objectsList = allobjects.getAllObjects()
        speakers = Speaker.objects.filter(speakerApproved=True)
        form = TalkForm()
    return render(request, 'talks/talkEdit.html', {'form': form, 'events':events, 'speakers':speakers, 'list': objectsList})

@login_required
def talkEdit(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    objectsList = allobjects.getAllObjects()
    userIsParticipant = False

    if hasattr(request.user, 'speaker'):
        userIsParticipant = talk.speakerId.filter(id=request.user.speaker.id).exists()

    if userIsParticipant or request.user.is_superuser:
        if request.method == "POST":
            form = TalkForm(request.POST, instance=talk)
            if form.is_valid():
                talk = form.save(commit=False)
                talk.save()
                form.save_m2m()
                return redirect('talkDetail', pk=talk.pk)
        else:
            events = Event.objects.all()
            speakers = Speaker.objects.filter(speakerApproved=True)
            form = TalkForm(instance=talk)
        return render(request, 'talks/talkEdit.html', {'form': form, 'events':events, 'speakers':speakers, 'new': "Editar", 'list': objectsList})
    else:
        return redirect('talkDetail', pk=talk.pk)

@login_required
@permission_required('is_superuser', 'eventList')
def talkRemove(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    talk.delete()
    return redirect('eventDetail', pk=talk.eventId.pk)

@login_required
@permission_required('is_superuser', 'eventList')
def talkApprove(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    talk.approve()
    return redirect('talkDetail', pk=talk.pk)