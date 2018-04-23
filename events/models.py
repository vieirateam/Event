from django.db import models
from django.utils import timezone
from speakers.models import Speaker

class Event(models.Model):
    eventName = models.CharField(verbose_name="Nome", max_length=300)
    eventDesc = models.TextField(verbose_name="Descrição")
    eventStartDate = models.DateField(verbose_name="Data de Abertura", default=timezone.now)
    eventFinishDate = models.DateField(verbose_name="Data de Encerramento")
    eventImage = models.ImageField(verbose_name="Imagem", blank=True, null=True)

    def approvedTalks(self):
        return self.talks.filter(talkApproved=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.eventName

class Talk(models.Model):
    eventId = models.ForeignKey(Event, verbose_name="Evento", related_name="talks")
    speakerId = models.ManyToManyField(Speaker, verbose_name="Palestrantes")
    talkName = models.CharField(verbose_name="Nome", max_length=300)
    talkType = models.CharField(verbose_name="Tipo", max_length=300)
    talkDesc = models.TextField(verbose_name="Descrição")
    talkMaxPeople = models.PositiveIntegerField(verbose_name="Quantidade Máxima de Participantes")
    talkDate = models.DateField(verbose_name="Data", default=timezone.now)
    talkStartTime = models.TimeField(verbose_name="Horário Inicial")
    talkFinishTime = models.TimeField(verbose_name="Horário Final")
    talkLocation = models.CharField(verbose_name="Localização", max_length=300)
    talkApproved = models.BooleanField(verbose_name="Aprovar", default=False)
    
    def approve(self):
        self.talkApproved = True
        self.save()