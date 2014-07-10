from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime

class BejegyzesManager(models.Manager):
	def get_honapok(self):
		honapok=set()
		bejegyzesek=super(BejegyzesManager, self).get_queryset().all()
		for b in bejegyzesek:
			honapok.add((b.ido.year, b.ido.month))
		datumok=[]
		for h in honapok:
			datumok.append(datetime.date(h[0], h[1],1))
		return datumok
# Create your models here.
class Cimke(models.Model):
	szoveg=models.CharField(max_length=512)
	szin=models.CharField(max_length=32)
	def get_absolute_url(self):
		return reverse('blogcucc_cimke', kwargs={'cimke': self.szoveg })
	def __unicode__(self):
		return self.szoveg
	def count_bejegyzes(self):
		return Bejegyzes.objects.filter(cimkek__in=[self]).count()
	class Meta:
		verbose_name_plural="Cimkek"
class Bejegyzes(models.Model):
	cim=models.CharField(max_length=512)
	szoveg=models.TextField()
	ido=models.DateTimeField(auto_now=True)
	irta=models.ForeignKey(User)
	cimkek=models.ManyToManyField(Cimke,blank=True)
	objects=BejegyzesManager()
	def get_absolute_url(self):
		return reverse('blogcucc_detailbejegyzes', kwargs={'pk': self.pk })
	def count_komment(self):
		return Komment.objects.filter(bejegyzes=self).count()
	def get_first_part(self):
		if self.szoveg.find("__LEVAG:LEVAG__")==-1:
			return self.szoveg
		return self.szoveg[0:self.szoveg.find("__LEVAG:LEVAG__")]
	class Meta:
		verbose_name_plural="Bejegyzesek"
		ordering=["-ido"]
class Komment(models.Model):
	szoveg=models.TextField()
	irta=models.ForeignKey(User, blank=True, null=True)
	ido=models.DateTimeField(auto_now=True)
	bejegyzes=models.ForeignKey(Bejegyzes)
	def get_absolute_url(self):
		return reverse('blogcucc_detailbejegyzes', kwargs={'pk':self.bejegyzes.pk})
	class Meta:
		verbose_name_plural="Kommentek"