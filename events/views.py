from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from rest_framework.decorators import api_view
from .models import Event, Talk, Speaker
from . import allobjects
from .forms import EventForm, TalkForm, ContactForm, SpeakerForm
from .serializers import EventSerializer, SpeakerSerializer, TalkSerializer


def home(request):
    objectsList = allobjects.getAllObjects()

    date = timezone.localdate()
    events = Event.objects.all().order_by('startDate')

    nowEvents = []
    for event in events:
        if event.startDate <= date <= event.finishDate:
            nowEvents.append(event)
        if len(nowEvents) == 4:
            break

    nextEvents = []
    for event in events:
        if event.startDate > date:
            nextEvents.append(event)
        if len(nextEvents) == 4:
            break

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
    return render(request, 'index.html',
                  {'form': emailForm, 'list': objectsList, 'nowEvents': nowEvents, 'nextEvents': nextEvents})


def pendencyList(request):
    if request.user.is_superuser:
        talksNotApproved = Talk.objects.filter(approved=False)
        speakersNotApproved = Speaker.objects.filter(approved=False)
        return render(request, 'pendencyList.html', {'talks': talksNotApproved, 'speakers': speakersNotApproved})
    return redirect('home')


def pendencyCountJson(request):
    if request.user.is_superuser:
        talksNotApproved = Talk.objects.filter(approved=False).count()
        speakersNotApproved = Speaker.objects.filter(approved=False).count()
        number = talksNotApproved + speakersNotApproved
        pendency_count = {
            'number': number,
        }
        return JsonResponse(pendency_count)


def eventList(request):
    events = Event.objects.all().order_by('startDate')
    return render(request, 'events/eventList.html', {'events': events})


@api_view(['GET'])
def eventListJson(request):
    if request.method == 'GET':
        events = Event.objects.all().order_by('startDate')
        serializer = EventSerializer(events, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def eventTalkListJson(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'GET':
        talks = event.talks.filter(approved=True).order_by('date')
        serializer = TalkSerializer(talks, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def nowEventListJson(request):
    if request.method == 'GET':
        date = timezone.localdate()
        events = Event.objects.all().order_by('startDate')
        nowEvents = []
        for event in events:
            if event.startDate <= date <= event.finishDate:
                nowEvents.append(event)

        serializer = EventSerializer(nowEvents, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def nextEventListJson(request):
    if request.method == 'GET':
        events = Event.objects.all().order_by('startDate')
        nextEvents = []
        for event in events:
            if event.startDate > timezone.localdate():
                nextEvents.append(event)
            if len(nextEvents) == 5:
                break

        serializer = EventSerializer(nextEvents, many=True)
        return JsonResponse(serializer.data, safe=False)


def eventDetail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/eventDetail.html', {'event': event})


@api_view(['GET'])
def eventDetailJson(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'GET':
        serializer = EventSerializer(event)
        return JsonResponse(serializer.data)


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
    return render(request, 'events/eventEdit.html', {'form': form, 'edit': "Editar", 'list': objectsList})


@login_required
@permission_required('is_superuser', 'eventList')
def eventRemove(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('eventList')


def speakerList(request):
    speakers = Speaker.objects.all().order_by('name')
    return render(request, 'speakers/speakerList.html', {'speakers': speakers})


@api_view(['GET'])
def speakerListJson(request):
    if request.method == 'GET':
        speakers = Speaker.objects.filter(approved=True).order_by('name')
        serializer = SpeakerSerializer(speakers, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def speakerTalkJson(request, pk):
    speaker = get_object_or_404(Speaker, pk=pk)
    if speaker.approved:
        if request.method == 'GET':
            talks = speaker.speakers.filter(approved=True).order_by('date')
            serializer = TalkSerializer(talks, many=True)
            return JsonResponse(serializer.data, safe=False)


def speakerDetail(request, pk):
    speaker = get_object_or_404(Speaker, pk=pk)
    if speaker.approved or request.user.is_authenticated:
        objectsList = allobjects.getAllObjects()
        return render(request, 'speakers/speakerDetail.html', {'speaker': speaker, 'list': objectsList})
    return redirect('speakerList')


@api_view(['GET'])
def speakerDetailJson(request, pk):
    speaker = get_object_or_404(Speaker, pk=pk)
    if speaker.approved:
        if request.method == 'GET':
            serializer = SpeakerSerializer(speaker)
            return JsonResponse(serializer.data)


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
    return JsonResponse({'status': 1})


@login_required
@permission_required('is_superuser', 'speakerList')
def speakerRemove(request, pk):
    speaker = get_object_or_404(Speaker, pk=pk)

    if not speaker.approved:
        speaker.user.delete()
        speaker.delete()
    return redirect('speakerList')


@api_view(['GET'])
def talkListJson(request):
    if request.method == 'GET':
        talks = Talk.objects.filter(approved=True).order_by('name')
        serializer = TalkSerializer(talks, many=True)
        return JsonResponse(serializer.data, safe=False)


def talkDetail(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    objectsList = allobjects.getAllObjects()
    if talk.approved or request.user.is_authenticated:
        userIsParticipant = False

        if hasattr(request.user, 'speaker'):
            userIsParticipant = talk.speakers.filter(id=request.user.speaker.id).exists()

        return render(request, 'talks/talkDetail.html',
                      {'talk': talk, 'userIsParticipant': userIsParticipant, 'list': objectsList})
    return redirect('eventDetail', pk=talk.eventId.pk)


@api_view(['GET'])
def talkDetailJson(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    if talk.approved:
        if request.method == 'GET':
            serializer = TalkSerializer(talk)
            return JsonResponse(serializer.data)


@api_view(['GET'])
def talkSpeakerJson(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    if request.method == 'GET':
        speakers = talk.speakers.filter(approved=True).order_by('name')
        serializer = SpeakerSerializer(speakers, many=True)
        return JsonResponse(serializer.data, safe=False)


@login_required
def talkNew(request):
    permission = False
    if hasattr(request.user, 'speaker'):
        if request.user.speaker.approved:
            permission = True

    if permission or request.user.is_superuser:
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
        return render(request, 'talks/talkEdit.html',
                      {'form': form, 'events': events, 'speakers': speakers, 'list': objectsList})
    return redirect('home')


@login_required
def talkEdit(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    objectsList = allobjects.getAllObjects()
    userIsParticipant = False

    if hasattr(request.user, 'speaker'):
        userIsParticipant = talk.speakers.filter(id=request.user.speaker.id).exists()

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
        return render(request, 'talks/talkEdit.html',
                      {'form': form, 'events': events, 'speakers': speakers, 'edit': "Editar", 'list': objectsList})
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
    return JsonResponse({'status': 1})


@api_view(['GET'])
def objectListJson(request):
    if request.method == 'GET':
        events = Event.objects.all().order_by('name')
        talks = Talk.objects.filter(approved=True).order_by('name')
        speakers = Speaker.objects.filter(approved=True).order_by('name')
        eventSerializer = EventSerializer(events, many=True)
        talkSerializer = TalkSerializer(talks, many=True)
        speakerSerializer = SpeakerSerializer(speakers, many=True)
        serializer = [eventSerializer.data, talkSerializer.data, speakerSerializer.data]
        return JsonResponse(serializer, safe=False)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            speaker = Speaker(user=user, name=username)
            speaker.id = user.id
            speaker.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
