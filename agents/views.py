from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from django.core.mail import send_mail

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
        agent = form.save(commit=False)
        agent.organisation = self.request.user.userprofile
        form.save()
        # TODO send Email
        send_mail(
            subject="An agent has been created", 
            message="Go to the site to see the new agent",
            from_email="test@test.com", 
            recipient_list=["test2@test.com"],
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



