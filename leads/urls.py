from django.urls import path
from .views import list_leads, lead_detail

app_name = "leads"

urlpatterns = [
    path('', list_leads),
    path('<pk>/', lead_detail),
]
