from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from encounters.models import Encounter, Patient, Facility, Physician
from encounters.tests import (
    TEST_ENCOUNTERS,
    TEST_PATIENTS,
    TEST_FACILITIES,
    TEST_PHYSICIANS,
)


class Command(BaseCommand):
    help = '''Add some default models for testing'''

    def handle(self, *args, **kwargs):
        try:
            get_user_model().objects.create_superuser('test', 'test@test.us', 'test')
        except Exception:
            pass
        try:
            get_user_model().objects.create_superuser('admin', 'admin@admin.us', 'admin')
        except Exception:
            pass
        [Facility.objects.update_or_create(**obj) for obj in TEST_FACILITIES]
        [Patient.objects.update_or_create(**obj) for obj in TEST_PATIENTS]
        [Physician.objects.update_or_create(**obj) for obj in TEST_PHYSICIANS]
        facility = Facility.objects.all().first()
        patient = Patient.objects.all().first()
        physician = Physician.objects.all().first()
        [Encounter.objects.update_or_create(patient=patient, facility=facility, physician=physician, **obj) for obj in TEST_ENCOUNTERS]
