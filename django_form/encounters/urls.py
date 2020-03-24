"""umc_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (
    PatientAutocomplete,
    PatientCreateView,
    PatientDeleteView,
    PatientDetailView,
    PatientListView,
    PhysicianAutocomplete,
    PhysicianCreateView,
    PhysicianDeleteView,
    PhysicianDetailView,
    PhysicianListView,
    FacilityAutocomplete,
    FacilityCreateView,
    FacilityDeleteView,
    FacilityDetailView,
    FacilityListView,
    EncounterCreateView,
    EncounterDeleteView,
    EncounterDetailView,
    EncounterListView,
)

urlpatterns = [
    path('create/', EncounterCreateView.as_view(), name='encounters-create'),
    path(
        'patients/autocomplete/',
        PatientAutocomplete.as_view(create_field='name'),
        name='patients-autocomplete',
    ),
    path('patients/create/', PatientCreateView.as_view(), name='patients-create'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patients-detail'),
    path('patients/<int:pk>/delete/', PatientDeleteView.as_view(), name='patients-delete'),
    path('patients/', PatientListView.as_view(), name='patients-list'),
    path(
        'physicians/autocomplete/',
        PhysicianAutocomplete.as_view(create_field='name'),
        name='physicians-autocomplete',
    ),
    path('physicians/create/', PhysicianCreateView.as_view(), name='physicians-create'),
    path('physicians/<int:pk>/', PhysicianDetailView.as_view(), name='physicians-detail'),
    path('physicians/<int:pk>/delete/', PhysicianDeleteView.as_view(), name='physicians-delete'),
    path('physicians/', PhysicianListView.as_view(), name='physicians-list'),
    path(
        'facilities/autocomplete/',
        FacilityAutocomplete.as_view(create_field='name'),
        name='facilities-autocomplete',
    ),
    path('facilities/create/', FacilityCreateView.as_view(), name='facilities-create'),
    path('facilities/<int:pk>/delete/', FacilityDeleteView.as_view(), name='facilities-delete'),
    path('facilities/<int:pk>/', FacilityDetailView.as_view(), name='facilities-detail'),
    path('facilities/', FacilityListView.as_view(), name='facilities-list'),
    path('<int:pk>/delete/', EncounterDeleteView.as_view(), name='encounters-delete'),
    path('<int:pk>/', EncounterDetailView.as_view(), name='encounters-detail'),
    path('', EncounterListView.as_view(), name='encounters-list'),
]
