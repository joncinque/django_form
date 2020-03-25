from django.db import models
from django.urls import reverse

MAX_NAME_LENGTH = 200
MAX_ADDRESS_LENGTH = 200
MAX_SSN_LENGTH = 15
MAX_PHONE_LENGTH = 30


class Sex(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'
    DECLINE = 'Decline to answer'


class EncounterType(models.TextChoices):
    INPATIENT = 'Inpatient'
    OUTPATIENT_AMBULANCE = 'Outpatient Ambulance'
    OUTPATIENT_OFFICE = 'Outpatient Office'


class Patient(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH, db_index=True)
    email = models.EmailField(blank=True)
    ssn = models.CharField(max_length=MAX_SSN_LENGTH, blank=True)
    address = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)
    city = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)
    state = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)
    zipcode = models.CharField(max_length=MAX_PHONE_LENGTH, blank=True)
    phone = models.CharField(max_length=MAX_PHONE_LENGTH, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    sex = models.CharField(
        max_length=MAX_PHONE_LENGTH,
        choices=Sex.choices,
        default=Sex.OTHER,
    )

    def get_absolute_url(self):
        return reverse('patients-detail', args=[self.id])

    def get_delete_url(self):
        return reverse('patients-delete', args=[self.id])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


class Facility(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH, db_index=True)
    email = models.EmailField(blank=True)
    taxid = models.CharField(max_length=MAX_SSN_LENGTH, blank=True)
    address = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)
    city = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)
    state = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)
    zipcode = models.CharField(max_length=MAX_PHONE_LENGTH, blank=True)
    phone = models.CharField(max_length=MAX_PHONE_LENGTH, blank=True)
    fax = models.CharField(max_length=MAX_PHONE_LENGTH, blank=True)
    admin = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)

    def get_absolute_url(self):
        return reverse('facilities-detail', args=[self.id])

    def get_delete_url(self):
        return reverse('facilities-delete', args=[self.id])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'


class Physician(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH, db_index=True)
    email = models.EmailField(blank=True)
    taxid = models.CharField(max_length=MAX_SSN_LENGTH, blank=True)
    address = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)
    city = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)
    state = models.CharField(max_length=MAX_NAME_LENGTH, blank=True)
    zipcode = models.CharField(max_length=MAX_PHONE_LENGTH, blank=True)
    phone = models.CharField(max_length=MAX_PHONE_LENGTH, blank=True)
    fax = models.CharField(max_length=MAX_PHONE_LENGTH, blank=True)

    def get_absolute_url(self):
        return reverse('physicians-detail', args=[self.id])

    def get_delete_url(self):
        return reverse('physicians-delete', args=[self.id])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Physician'
        verbose_name_plural = 'Physicians'


class Encounter(models.Model):
    requested_type = models.CharField(
        max_length=MAX_PHONE_LENGTH,
        choices=EncounterType.choices,
        default=EncounterType.INPATIENT,
    )
    assigned_type = models.CharField(
        max_length=MAX_PHONE_LENGTH,
        choices=EncounterType.choices,
        default=EncounterType.INPATIENT,
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    charting = models.TextField(blank=True)  # TODO formset
    reviews = models.TextField(null=True, blank=True)  # TODO formset

    def get_absolute_url(self):
        return reverse('encounters-detail', args=[self.id])

    def get_delete_url(self):
        return reverse('encounters-delete', args=[self.id])

    def __str__(self):
        return self.created.strftime('%Y/%m/%d %H:%M') + ' - ' + self.patient.name

    class Meta:
        ordering = ['last_modified', 'created']
        verbose_name = 'Encounter'
        verbose_name_plural = 'Encounters'
