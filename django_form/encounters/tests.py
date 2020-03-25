from datetime import date, datetime, timedelta, timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import PatientForm
from .models import Facility, Patient, Physician, Encounter

TEST_PATIENT1 = {
    'name': 'TestPatient1',
    'email': 'test1@patient.com',
    'ssn': 'xxx-xx-xxxx',
    'phone': '(xxx) xxx-xxxx',
    'address': '123 Fake Street',
    'city': 'Springfield',
    'state': 'NV',
    'zipcode': '10001',
    'birthdate': date(1950, 12, 2),
}
TEST_PATIENT2 = {
    'name': 'TestPatient2',
    'email': 'test2@patient.com',
    'ssn': 'xxx-xx-xxxx',
    'phone': '(xxx) xxx-xxxx',
    'address': '1 Real Lane',
    'city': 'Spring',
    'state': 'TX',
    'zip': '10002',
}
TEST_PATIENT3 = {
    'name': 'TestPatient3',
    'email': 'test3@patient.com',
    'ssn': 'xxx-xx-xxxx',
    'phone': '(xxx) xxx-xxxx',
    'address': '142 Some Street',
    'city': 'Spring',
    'state': 'TX',
    'zip': '10002',
}
TEST_PATIENTS = [TEST_PATIENT1, TEST_PATIENT2, TEST_PATIENT3]

TEST_FACILITY1 = {
    'name': 'Facility1',
    'admin': 'Admin1',
    'address': 'Address1',
    'phone': '(111) 111-1111',
}
TEST_FACILITY2 = {
    'name': 'Facility2',
    'admin': 'Admin2',
    'address': 'Address2',
    'phone': '(222) 222-2222',
}
TEST_FACILITIES = [TEST_FACILITY1, TEST_FACILITY2]


TEST_PHYSICIAN1 = {
    'name': 'Physician1',
    'address': 'Address1',
    'phone': '(111) 111-1111',
}
TEST_PHYSICIAN2 = {
    'name': 'Physician2',
    'address': 'Address2',
    'phone': '(222) 222-2222',
}
TEST_PHYSICIANS = [TEST_PHYSICIAN1, TEST_PHYSICIAN2]


TEST_ENCOUNTERS = [
    {
        'charting': 'Lots of useful information here in free-form',
        'created': datetime.now(tz=timezone.utc),
        'last_modified': datetime.now(tz=timezone.utc),
    },
    {
        'charting': 'There was a lot of information to keep track of here.',
        'created': datetime.now(tz=timezone.utc) - timedelta(days=2),
        'last_modified': datetime.now(tz=timezone.utc) - timedelta(days=1),
    },
]


class PatientFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        [Patient.objects.create(**patient) for patient in TEST_PATIENTS]

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
        patient_object = Patient.objects.filter(name=TEST_PATIENT2['name']).first()
        for k, v in TEST_PATIENT2.items():
            self.assertEqual(getattr(patient_object, k), v)
        form = PatientForm(instance=patient_object)
        new_email = 'newemail@test.com'
        form.data['email'] = new_email


class PhysicianFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        [Physician.objects.create(**obj) for obj in TEST_PHYSICIANS]


class FacilityFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        [Facility.objects.create(**obj) for obj in TEST_FACILITIES]


class EncounterFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        [Patient.objects.create(**patient) for patient in TEST_PATIENTS]
        [Facility.objects.create(**obj) for obj in TEST_FACILITIES]
        [Physician.objects.create(**obj) for obj in TEST_PHYSICIANS]
        facility = Facility.objects.all().first()
        patient = Patient.objects.all().first()
        physician = Physician.objects.all().first()
        [Encounter.objects.update_or_create(patient=patient, facility=facility, physician=physician, **obj) for obj in TEST_ENCOUNTERS]

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
