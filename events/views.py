from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Talk, Speaker
from . import allobjects
from .forms import EventForm, TalkForm, ContactForm, SpeakerForm

def home(request):
    objectsList = allobjects.getAllObjects()
    nextEvents = Event.objects.all().order_by('startDate')[:4]
    
    if request.method == 'GET':
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
        talksNotApproved = Talk.objects.filter(approved=False)
        speakersNotApproved = Speaker.objects.filter(approved=False)
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
    objectsList = allobjects.getAllObjects()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('eventDetail', pk=event.pk)
    else:
        form = EventForm()
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

def speakerList(request):
    objectsList = allobjects.getAllObjects()
    speakers = Speaker.objects.all().order_by('name')
    return render(request, 'speakers/speakerList.html', {'speakers': speakers, 'list': objectsList})

def speakerDetail(request, pk):
	speaker = get_object_or_404(Speaker, pk=pk)
	objectsList = allobjects.getAllObjects()
	return render(request, 'speakers/speakerDetail.html', {'speaker': speaker, 'list': objectsList})

@login_required
def speakerEdit(request, pk):
    speaker = get_object_or_404(Speaker, pk=pk)
    objectsList = allobjects.getAllObjects()
    if speaker.id != request.user.id:
    	return redirect('speakerDetail', pk=speaker.pk)
    if request.method == "POST":
        form = SpeakerForm(request.POST, request.FILES, instance=speaker)
        if form.is_valid():
            speaker = form.save(commit=False)
            speaker.user = request.user
            speaker.save()
            return redirect('speakerDetail', pk=speaker.pk)
    else:
        form = SpeakerForm(instance=speaker)
    return render(request, 'speakers/speakerEdit.html', {'form': form, 'list': objectsList})

@login_required
@permission_required('is_superuser', 'speakerList')
def speakerApprove(request, pk):
    speaker = get_object_or_404(Speaker, pk=pk)
    speaker.approve()
    return redirect('speakerDetail', pk=speaker.pk)

@login_required
@permission_required('is_superuser', 'speakerList')
def speakerRemove(request, pk):
    speaker = get_object_or_404(Speaker, pk=pk)
    speaker.user.delete()
    speaker.delete()
    return redirect('speakerList')  

def talkDetail(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    objectsList = allobjects.getAllObjects()
    if talk.approved or request.user.is_authenticated:
        userIsParticipant = False
        
        if hasattr(request.user, 'speaker'):
            userIsParticipant = talk.speakerId.filter(id=request.user.speaker.id).exists()
        
        return render(request, 'talks/talkDetail.html', {'talk': talk, 'userIsParticipant': userIsParticipant, 'list': objectsList})
    return redirect('eventDetail', pk=talk.eventId.pk)

@login_required
def talkNew(request):
    events = Event.objects.all()
    objectsList = allobjects.getAllObjects()
    speakers = Speaker.objects.filter(approved=True)
    if request.method == "POST":
        form = TalkForm(request.POST)
        if form.is_valid():
            talk = form.save(commit=False)
            talk.save()
            form.save_m2m()
            return redirect('talkDetail', pk=talk.pk)
    else:
        form = TalkForm()
    return render(request, 'talks/talkEdit.html', {'form': form, 'events':events, 'speakers':speakers, 'list': objectsList})

@login_required
def talkEdit(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    objectsList = allobjects.getAllObjects()
    userIsParticipant = False

    if hasattr(request.user, 'speaker'):
        userIsParticipant = talk.speakers.filter(id=request.user.id).exists()

    if userIsParticipant or request.user.is_superuser:
        events = Event.objects.all()
        speakers = Speaker.objects.filter(approved=True)
        if request.method == "POST":
            form = TalkForm(request.POST, instance=talk)
            if form.is_valid():
                talk = form.save(commit=False)
                talk.save()
                form.save_m2m()
                return redirect('talkDetail', pk=talk.pk)
        else:
            form = TalkForm(instance=talk)
        return render(request, 'talks/talkEdit.html', {'form': form, 'events':events, 'speakers':speakers, 'new': "Editar", 'list': objectsList})
    else:
        return redirect('talkDetail', pk=talk.pk)

@login_required
@permission_required('is_superuser', 'eventList')
def talkRemove(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    talk.delete()
    return redirect('eventDetail', pk=talk.event.pk)

@login_required
@permission_required('is_superuser', 'eventList')
def talkApprove(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    talk.approve()
    return redirect('talkDetail', pk=talk.pk)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            speaker = Speaker(user=user,name=username)
            speaker.id = user.id
            speaker.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



