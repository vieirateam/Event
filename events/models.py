from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=300)
    desc = models.TextField()
    startDate = models.DateField(default=timezone.localdate)
    finishDate = models.DateField()
    image = models.ImageField(blank=True, null=True)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    def approvedTalks(self):
        return self.talks.filter(approved=True)

    def approvedSpeakers(self):
        return self.speakers.filter(approved=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name

class Speaker(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=300)
	email = models.EmailField()
	formation = models.CharField(max_length=300)
	bio = models.TextField()
	image = models.ImageField(blank=True, null=True)
	approved = models.BooleanField(default=False)

	def approve(self):
		self.approved = True
		self.save()

	def __str__(self):
		return self.name

class Talk(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="talks")
    speakers = models.ManyToManyField(Speaker, related_name="speakers")
    name = models.CharField(max_length=300)
    category = models.CharField(max_length=300)
    desc = models.TextField()
    maxPeople = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)
    startTime = models.TimeField()
    finishTime = models.TimeField()
    location = models.CharField(max_length=300)
    approved = models.BooleanField(default=False)
    
    def approve(self):
        self.approved = True
        self.save()
