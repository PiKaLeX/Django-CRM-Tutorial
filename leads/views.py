from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm
from agents.mixins import OrganisorAndLoginRequiredMixin

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

def landing_page(request):
    return render(request, "landing.html")


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
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else: # Agent
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the current agent only
            queryset = queryset.filter(agent__user=user)   
        return queryset

def list_leads(request):
    leads = Lead.objects.all()

    context = {
        "leads": leads
    }
    return render(request, "leads/list_leads.html", context=context)




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

def lead_detail(request, pk):
    
    lead = Lead.objects.get(id=pk)

    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context=context)




class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        # TODO send Email
        send_mail(
            subject="A lead has been created", 
            message="Go to the site to see the new lead",
            from_email="test@test.com", 
            recipient_list=["test2@test.com", "pikalex1@hotmail.com"],
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()

    if request.method == "POST":
        #print('receiving a post request')
        form = LeadModelForm(request.POST)

        if form.is_valid():
            #print('Form is valid')
            #print(form.cleaned_data)

            # All of this is equivalent to  form.save() now that we use the modelForm
                # first_name = form.cleaned_data['first_name']
                # last_name = form.cleaned_data['last_name']
                # age = form.cleaned_data['age']
                # agent = form.cleaned_data['agent']

                # Lead.objects.create(
                #     first_name=first_name,
                #     last_name=last_name, 
                #     age=age, 
                #     agent=agent
                # )
            form.save()


            #print('Lead has been created.')

            return redirect("/leads")

    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context=context)




class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user    
        return Lead.objects.filter(organisation=user.userprofile) 

    def get_success_url(self):
        return reverse('leads:lead-list')

def lead_update(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)

    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)

        if form.is_valid():            
            form.save()
            return redirect("/leads")

    context = {
        "lead": lead,
        "form": form,
    }
    return render(request, "leads/lead_update.html", context=context)






class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_queryset(self):
        user = self.request.user    
        return Lead.objects.filter(organisation=user.userprofile) 

    def get_success_url(self):
        return reverse('leads:lead-list')

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()    
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
            
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
            
#             lead.first_name=first_name
#             lead.last_name=last_name
#             lead.age=age

#             lead.save()
#             print('Lead has been updated.')

#             return redirect("/leads")

#     context = {
#         "lead": lead,
#         "form": form,
#     }
#     return render(request, "leads/lead_update.html", context=context)


# def lead_create(request):
#     form = LeadForm()

#     if request.method == "POST":
#         #print('receiving a post request')
#         form = LeadForm(request.POST)

#         if form.is_valid():
#             #print('Form is valid')
#             #print(form.cleaned_data)

#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']

#             agent = Agent.objects.first()

#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name, 
#                 age=age, 
#                 agent=agent
#             )
#             #print('Lead has been created.')

#             return redirect("/leads")

#     context = {
#         "form": form
#     }
#     return render(request, "leads/lead_create.html", context=context)
