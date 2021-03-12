from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from django.core.mail import send_mail

from random import randrange

from leads.models import Agent
from .forms import  AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin

class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    context_object_name = 'agents' 
    template_name = "agents/agents_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agents_detail.html"
    context_object_name = 'agent'
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "Agents/Agents_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agents-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{randrange(1000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        #agent.organisation = self.request.user.userprofile
        #form.save()
        # TODO send Email
        send_mail(
            subject="You are invited ot be an Agent", 
            message="you were added as an agent on DJCRM. Please come login to start working.",
            from_email="organiser@djcrm.com", 
            recipient_list=[user.email],
        )
        return super(AgentCreateView, self).form_valid(form)

class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "Agents/Agents_update.html"
    form_class = AgentModelForm
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse('agents:agents-list')

class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "Agents/Agents_delete.html"
        
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse('agents:agents-list')



