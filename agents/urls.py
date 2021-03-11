from django.urls import path
from .views import (
    AgentListView, AgentDetailView, AgentCreateView, AgentUpdateView, AgentDeleteView
)

app_name = "agents"

urlpatterns = [
    path('', AgentListView.as_view(), name='agents-list'),
    path('<int:pk>/', AgentDetailView.as_view(), name='agents-detail'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='agents-update'),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name='agents-delete'),
    path('create/', AgentCreateView.as_view(), name='agents-create'),
]
