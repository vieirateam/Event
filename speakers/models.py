from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Speaker(models.Model):
	speakerId = models.OneToOneField(User, on_delete=models.CASCADE)
	speakerName = models.CharField(verbose_name="Nome", max_length=300)
	speakerEmail = models.EmailField(verbose_name="Email")
	speakerFormation = models.CharField(verbose_name="Formação", max_length=300)
	speakerBio = models.TextField(verbose_name="Biografia")
	speakerImage = models.ImageField(verbose_name="Imagem", blank=True, null=True)
	speakerApproved = models.BooleanField(verbose_name="Aprovar", default=False)

	def approve(self):
		self.speakerApproved = True
		self.save()

	def __str__(self):
		return self.speakerName