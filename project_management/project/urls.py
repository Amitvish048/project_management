from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:id>/', views.ClientRetrieveUpdateDestroyView.as_view(), name='client-retrieve-update-destroy'),
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:id>/', views.ProjectDeleteView.as_view(), name='project-delete'),

]