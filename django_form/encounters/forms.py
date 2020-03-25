from dal import autocomplete
from django import forms

from .models import Patient, Physician, Facility, Encounter


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ()


class PhysicianForm(forms.ModelForm):
    class Meta:
        model = Physician
        exclude = ()


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        exclude = ()


class EncounterForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='patients-autocomplete',
            attrs={
                'data-scroll-after-select': 'true',
                'data-container-css-class': 'encounters-select2',
            })
    )
    facility = forms.ModelChoiceField(
        queryset=Facility.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='facilities-autocomplete',
            attrs={
                'data-scroll-after-select': 'true',
                'data-container-css-class': 'encounters-select2',
            })
    )
    physician = forms.ModelChoiceField(
        queryset=Physician.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='physicians-autocomplete',
            attrs={
                'data-scroll-after-select': 'true',
                'data-container-css-class': 'encounters-select2',
            })
    )

    class Meta:
        model = Encounter
        exclude = ()
