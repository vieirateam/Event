from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from .models import Event, Talk
from speakers.models import Speaker
from .forms import EventForm, TalkForm, ContactForm

def home(request):
    emailForm = ContactForm()
    events = Event.objects.all().order_by('eventStartDate')[:4]
    return render(request, 'index.html', {'events': events, 'form': emailForm}) 

def pendencyList(request):
    if request.user.is_superuser:
        talksNotApproved = Talk.objects.filter(talkApproved=False)
        return render(request, 'pendencyList.html', {'talks': talksNotApproved})
    return redirect('eventList')

def eventList(request):
    events = Event.objects.all().order_by('eventStartDate')
    return render(request, 'events/eventList.html', {'events': events})

def eventDetail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/eventDetail.html', {'event': event})

@login_required
def eventNew(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                event = form.save(commit=False)
                event.save()
                return redirect('eventDetail', pk=event.pk)
        else:
            form = EventForm()
        return render(request, 'events/eventEdit.html', {'form': form})
    else:
        return redirect('eventList')

@login_required
def eventEdit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user.is_superuser:
        if request.method == "POST":
            form = EventForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                event = form.save(commit=False)
                event.save()
                return redirect('eventDetail', pk=event.pk)
        else:
            form = EventForm(instance=event)
        return render(request, 'events/eventEdit.html', {'form': form, 'new': "Editar"})
    else:
        return redirect('eventList')

@login_required
def eventRemove(request, pk):
    if request.user.is_superuser:
        event = get_object_or_404(Event, pk=pk)
        event.delete()

    return redirect('eventList')

def talkDetail(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    if talk.talkApproved or request.user.is_authenticated:
        userIsParticipant = False
        if not request.user.is_superuser:
            userIsParticipant = talk.speakerId.filter(id=request.user.speaker.id).exists()
        return render(request, 'talks/talkDetail.html', {'talk': talk, 'userIsParticipant': userIsParticipant})
    return redirect('eventDetail', pk=talk.eventId.pk)

@login_required
def talkNew(request):
    if request.method == "POST":
        form = TalkForm(request.POST)
        if form.is_valid():
            talk = form.save(commit=False)
            talk.save()
            form.save_m2m()
            return redirect('talkDetail', pk=talk.pk)
    else:
        events = Event.objects.all()
        speakers = Speaker.objects.filter(speakerApproved=True)
        form = TalkForm()
    return render(request, 'talks/talkEdit.html', {'form': form, 'events':events, 'speakers':speakers})

@login_required
def talkEdit(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    userIsParticipant = False

    if not request.user.is_superuser:
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
        return render(request, 'talks/talkEdit.html', {'form': form, 'events':events, 'speakers':speakers, 'new': "Editar"})
    else:
        return redirect('talkDetail', pk=talk.pk)

@login_required
def talkRemove(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    if request.user.is_superuser:
        talk.delete()
        return redirect('eventDetail', pk=talk.eventId.pk)
    else:
        return redirect('talkDetail', pk=talk.pk)

@login_required
def talkApprove(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    if request.user.is_superuser:
        talk.approve()

    return redirect('talkDetail', pk=talk.pk)

def contact(request):
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
    return render(request, 'index.html', {'form': emailForm})

