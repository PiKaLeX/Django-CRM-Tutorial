from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Lead, Agent, Category
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateModelForm
from agents.mixins import OrganisorAndLoginRequiredMixin

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/list_leads.html"
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user

        # Initial query set of Leads under the organisation
        if user.is_organisor:      
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False,
                )
        else: # Agent
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation,
                agent__isnull=False,
                )
            # filter for the current agent only
            queryset = queryset.filter(agent__user=user)   
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organisor:             
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                "unassigned_leads":queryset
            })
        return context

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = 'lead'
    
    def get_queryset(self):
        user = self.request.user

        # Initial query set of Leads under the organisation
        if user.is_organisor:      
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else: # Agent
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the current agent only
            queryset = queryset.filter(agent__user=user)   
        return queryset

class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.organisation=self.request.user.userprofile
        user.save()
        send_mail(
            subject="A lead has been created", 
            message="Go to the site to see the new lead",
            from_email="test@test.com", 
            recipient_list=["test2@test.com", "pikalex1@hotmail.com"],
        )
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        organisation = self.request.user.userprofile  
        return Lead.objects.filter(organisation=organisation) 

    def get_success_url(self):
        return reverse('leads:lead-list')

class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_queryset(self):
        user = self.request.user    
        return Lead.objects.filter(organisation=user.userprofile) 

    def get_success_url(self):
        return reverse('leads:lead-list')

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign-agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)

        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent  
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = 'category_list'

    def get_queryset(self):
        user = self.request.user

        # Initial query set of Leads under the organisation
        if user.is_organisor:      
            queryset = Category.objects.filter(
                organisation=user.userprofile
                )
        else: # Agent
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
                )  
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryListView, self).get_context_data(**kwargs)            
        if user.is_organisor:             
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:        
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_leads_count":queryset.filter(category__isnull=True).count()
        })
        return context

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user

        # Initial query set of Category under the organisation
        if user.is_organisor:      
            queryset = Category.objects.filter(
                organisation=user.userprofile
                )
        else: # Agent
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
                )  
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)            
        
    #     # 3 ways to get all the leads with the current categories. Explanation around 7h05 min in the video.
    #     qs = Lead.objects.filter(category=self.get_object()) # The usual way
    #     leads = self.get_object().leads.all() # same as above but with related name in our model
    #     # Can even be done within the template
    #     context.update({
    #         "leads":leads
    #     })
    #     return context

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateModelForm

    def get_queryset(self):
        user = self.request.user

        # Initial query set of Leads under the organisation
        if user.is_organisor:      
            queryset = Lead.objects.filter(
                organisation=user.userprofile
                )
        else: # Agent
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
                )  
        return queryset

    def get_success_url(self):
        return reverse('leads:lead-detail', kwargs={"pk": self.get_object().id})