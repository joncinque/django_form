from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import PatientForm
from .models import Patient

TEST_PATIENT1 = {
    'name': 'TestPatient1',
    'email': 'test1@patient.com',
    'ssn': 'xxx-xx-xxxx',
    'phone': '(xxx) xxx-xxxx',
}
TEST_PATIENT2 = {
    'name': 'TestPatient2',
    'email': 'test2@patient.com',
    'ssn': 'xxx-xx-xxxx',
    'phone': '(xxx) xxx-xxxx',
}
TEST_PATIENT3 = {
    'name': 'TestPatient3',
    'email': 'test3@patient.com',
    'ssn': 'xxx-xx-xxxx',
    'phone': '(xxx) xxx-xxxx',
}
TEST_PATIENTS = [TEST_PATIENT1, TEST_PATIENT2, TEST_PATIENT3]


class PatientFormTest(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.email = 'testuser@example.com'
        self.user = get_user_model().objects.create_user(self.username, self.email, self.password)
        self.client.login(username=self.username, password=self.password)

    def test_create(self):
        list_url = reverse('patients-list')
        patients_view = self.client.get(list_url)
        initial_patients = list(patients_view.context['patient_list'])
        create_url = reverse('patients-create')
        new_patient_response = self.client.post(create_url, data=TEST_PATIENT1)
        self.assertEqual(new_patient_response.status_code, 302)
        patient_url = new_patient_response['Location']
        patient_view = self.client.get(patient_url)
        patient = patient_view.context['patient']
        for k, v in TEST_PATIENT1.items():
            self.assertEqual(getattr(patient, k), v)
        patients_view = self.client.get(list_url)
        final_patients = list(patients_view.context['patient_list'])
        self.assertEqual(len(initial_patients) + 1, len(final_patients))

    def test_create_blank(self):
        create_url = reverse('patients-create')
        new_patient_response = self.client.post(create_url, data={})
        self.assertEqual(new_patient_response.context['field_errors'], ['This field is required.'])

    def test_modify(self):
        form = PatientForm(TEST_PATIENT2)
        self.assertTrue(form.is_valid())
        form.save()
        patient_object = Patient.objects.get(name=TEST_PATIENT2['name'])
        for k, v in TEST_PATIENT2.items():
            self.assertEqual(getattr(patient_object, k), v)
        form = PatientForm(instance=patient_object)
        new_email = 'newemail@test.com'
        form.data['email'] = new_email


class EncounterFormTest(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.email = 'testuser@example.com'
        self.user = get_user_model().objects.create_user(self.username, self.email, self.password)
        self.client.login(username=self.username, password=self.password)

    def test_create(self):
        list_url = reverse('encounters-list')
        list_view = self.client.get(list_url)
        initial = list(list_view.context['object_list'])
        self.assertIsInstance(initial, list)
        create_url = reverse('encounters-create')
        form_response = self.client.get(create_url)
        self.assertEqual(form_response.status_code, 200)
        print(list(form_response.context.keys()))
        print(form_response.context['form'])
