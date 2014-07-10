from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, View, TemplateView, UpdateView
from django.shortcuts import get_object_or_404
from django.forms.models import modelform_factory
from braces.views import CsrfExemptMixin, OrderableListMixin, LoginRequiredMixin, SuperuserRequiredMixin
from models import Bejegyzes, Komment, Cimke
from django.views.generic.dates import MonthArchiveView
class OldalCimkeHonapMixin(object):
	def get_context_data(self, **kwargs):
		context=super(OldalCimkeHonapMixin, self).get_context_data(**kwargs)
		context['cimkek']=Cimke.objects.all()
		context['honapok']=Bejegyzes.objects.get_honapok()
		return context
# Create your views here.
class BejegyzesList(OldalCimkeHonapMixin,ListView):
	model=Bejegyzes
	context_object_name="bejegyzesek"
class BejegyzesByCimke(OldalCimkeHonapMixin, ListView):
	model=Bejegyzes
	context_object_name="bejegyzesek"
	def get_queryset(self):
		cimke=get_object_or_404(Cimke, szoveg=self.kwargs['cimke'])
		return Bejegyzes.objects.filter(cimkek__in=[cimke])
class BejegyzesHonap(OldalCimkeHonapMixin, MonthArchiveView):
	model=Bejegyzes
	context_object_name="bejegyzesek"
	date_field="ido"
	template_name="blogcucc/bejegyzes_list.html"
class BejegyzesCreate(CsrfExemptMixin, LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
	model=Bejegyzes
	fields=["cim", "szoveg", "cimkek"]
	def form_valid(self, form):
		form.instance.irta=self.request.user
		return super(BejegyzesCreate, self).form_valid(form)
class BejegyzesDetail(OldalCimkeHonapMixin, DetailView):
	model=Bejegyzes
	def get_context_data(self, **kwargs):
		context=super(BejegyzesDetail, self).get_context_data(**kwargs)
		context['kommentform']=modelform_factory(Komment, fields=["szoveg"])
		context['kommentek']=Komment.objects.filter(bejegyzes=context["bejegyzes"])
		return context
class BejegyzesUpdate(CsrfExemptMixin, LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
	model=Bejegyzes
	fields=["cim", "szoveg", "cimkek"]
	def form_valid(self, form):
		form.instance.irta=self.request.user
		return super(BejegyzesUpdate, self).form_valid(form)
class CimkeCreate(CsrfExemptMixin, LoginRequiredMixin, CreateView):
	model=Cimke
class KommentCreate(CsrfExemptMixin, CreateView):
	model=Komment
	fields=["szoveg"]
	def form_valid(self, form):
		bejegyzes=get_object_or_404(Bejegyzes, pk=self.kwargs["bejegyzes"])
		form.instance.bejegyzes=bejegyzes
		form.instance.irta=self.request.user
		return super(KommentCreate, self).form_valid(form)
