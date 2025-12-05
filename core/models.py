from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_ADMIN = "admin"
    ROLE_DIRECTOR = "director"
    ROLE_DOCTOR = "doctor"
    ROLE_PATIENT = "patient"

    ROLE_CHOICES = [
        (ROLE_ADMIN, "Администратор"),
        (ROLE_DIRECTOR, "Директор"),
        (ROLE_DOCTOR, "Врач"),
        (ROLE_PATIENT, "Пациент"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_PATIENT)
    gender = models.CharField(max_length=10, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)

    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser

    def is_director(self):
        return self.role == self.ROLE_DIRECTOR

    def is_doctor(self):
        return self.role == self.ROLE_DOCTOR

    def is_patient(self):
        return self.role == self.ROLE_PATIENT


class Branch(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    director = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="directed_branches")

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    specialization = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    phone = models.CharField(max_length=50, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Appointment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_DONE = "done"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Ожидает"),
        (STATUS_CONFIRMED, "Подтверждён"),
        (STATUS_DONE, "Завершён"),
        (STATUS_CANCELLED, "Отменён"),
    ]

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="appointments")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="appointments")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_time} - {self.doctor} / {self.patient}"
