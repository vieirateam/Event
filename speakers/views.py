from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from events import allobjects
from django.utils import timezone
from .models import Speaker
from .forms import SpeakerForm

def speakerList(request):
    objectsList = allobjects.getAllObjects()
    speakers = Speaker.objects.all().order_by('speakerName')
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
            speaker.speakerId = request.user
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
    speaker.speakerId.delete()
    speaker.delete()
    return redirect('speakerList')  

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            speaker = Speaker(speakerId=user,speakerName="(Sem nome)")
            speaker.id = user.id
            speaker.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
