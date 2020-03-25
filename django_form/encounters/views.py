from dal import autocomplete
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Patient, Facility, Physician, Encounter
from .forms import EncounterForm, PatientForm, PhysicianForm, FacilityForm


class NameListView(ListView):
    model = None

    def get_queryset(self):
        if self.model is None:
            raise Exception('Model class not provided on NameListView')

        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(name__icontains=query)
            )
            return object_list
        else:
            return self.model.objects.all()


class EncounterCreateView(CreateView):
    model = Encounter
    form_class = EncounterForm
    template_name = 'encounters/encounter_form.html'

    def get_context_data(self, **kwargs):
        patient_form = PatientForm(prefix='patient_form')
        physician_form = PhysicianForm(prefix='physician_form')
        facility_form = FacilityForm(prefix='facility_form')
        return super().get_context_data(patient_form=patient_form,
                                        physician_form=physician_form,
                                        facility_form=facility_form)


class EncounterDetailView(UpdateView):
    model = Encounter
    form_class = EncounterForm
    success_url = reverse_lazy('encounters-list')
    template_name = 'encounters/encounter_form.html'

    def get_context_data(self, **kwargs):
        patient_form = PatientForm(prefix='patient_form')
        physician_form = PhysicianForm(prefix='physician_form')
        facility_form = FacilityForm(prefix='facility_form')
        return super().get_context_data(patient_form=patient_form,
                                        physician_form=physician_form,
                                        facility_form=facility_form)


class EncounterDeleteView(DeleteView):
    model = Encounter
    template_name = 'encounters/confirm_delete.html'
    success_url = reverse_lazy('encounters-list')


class EncounterListView(ListView):
    model = Encounter

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(patient__name__icontains=query)
            )
            return object_list
        else:
            return self.model.objects.all()


class PatientCreateView(CreateView):
    model = Patient
    template_name = 'encounters/form.html'
    form_class = PatientForm


class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'encounters/confirm_delete.html'
    success_url = reverse_lazy('patients-list')


class PatientDetailView(UpdateView):
    model = Patient
    template_name = 'encounters/form.html'
    form_class = PatientForm


class PatientListView(NameListView):
    model = Patient


class PhysicianCreateView(CreateView):
    model = Physician
    template_name = 'encounters/form.html'
    form_class = PhysicianForm


class PhysicianDeleteView(DeleteView):
    model = Physician
    template_name = 'encounters/confirm_delete.html'
    success_url = reverse_lazy('physicians-list')


class PhysicianDetailView(UpdateView):
    model = Physician
    template_name = 'encounters/form.html'
    form_class = PhysicianForm


class PhysicianListView(NameListView):
    model = Physician


class FacilityCreateView(CreateView):
    model = Physician
    template_name = 'encounters/form.html'
    form_class = FacilityForm


class FacilityDeleteView(DeleteView):
    model = Facility
    template_name = 'encounters/confirm_delete.html'
    success_url = reverse_lazy('facilities-list')


class FacilityDetailView(UpdateView):
    model = Facility
    template_name = 'encounters/form.html'
    form_class = FacilityForm


class FacilityListView(NameListView):
    model = Facility


class NameAutocomplete(autocomplete.Select2QuerySetView):
    model = None

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.model:
            raise Exception('NameAutocomplete used without setting model')

#        if not self.request.user.is_authenticated():
#            return self.model.objects.none()

        qs = self.model.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class PatientAutocomplete(NameAutocomplete):
    model = Patient


class PhysicianAutocomplete(NameAutocomplete):
    model = Physician


class FacilityAutocomplete(NameAutocomplete):
    model = Facility
