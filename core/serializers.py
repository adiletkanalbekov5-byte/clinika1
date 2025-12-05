from rest_framework import serializers
from .models import User, Branch, DoctorProfile, PatientProfile, Appointment

# ---------------- User ----------------
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"  # все поля для деталей, POST, PATCH


# ---------------- Branch ----------------
class BranchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "phone", "director"]  # только 4 поля для списка

class BranchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"  # все поля


# ---------------- Doctor ----------------
class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ["id", "user", "branch", "specialization"]

class DoctorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = "__all__"


# ---------------- Patient ----------------
class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ["id", "user", "phone", "birthdate"]

class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = "__all__"


# ---------------- Appointment ----------------
class AppointmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["id", "doctor", "patient", "date_time"]

class AppointmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
