from rest_framework import serializers
from .models import User, Branch, DoctorProfile, PatientProfile, Appointment

# ------------------- User -------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "role", "gender", "birthdate", "phone", "address", "tags"]

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]  # только 4 поля для списка

# ------------------- Branch -------------------
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

class BranchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "address", "phone"]

# ------------------- Doctor -------------------
class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DoctorProfile
        fields = ["id", "user", "branch", "specialization"]

class DoctorListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = ["id", "user", "branch", "specialization"]  # только 4 поля

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

# ------------------- Patient -------------------
class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PatientProfile
        fields = [
            "id", "user", "phone", "birthdate", "address", "complaints",
            "doctor", "date_time"
        ]  # все поля для POST/PUT/деталей

# core/serializers.py
# core/serializers.py
from rest_framework import serializers
from .models import PatientProfile

class PatientListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = PatientProfile
        fields = ["id", "full_name", "phone", "birthdate"]

    def get_full_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return ""




# ------------------- Appointment -------------------
class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField(read_only=True)
    patient = serializers.StringRelatedField(read_only=True)
    branch = serializers.StringRelatedField(read_only=True)

    doctor_id = serializers.PrimaryKeyRelatedField(queryset=DoctorProfile.objects.all(), source="doctor", write_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=PatientProfile.objects.all(), source="patient", write_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), source="branch", write_only=True, allow_null=True, required=False)

    class Meta:
        model = Appointment
        fields = ["id", "doctor", "doctor_id", "patient", "patient_id", "branch", "branch_id", "date_time", "status", "notes", "created_at"]

class AppointmentListSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ["id", "doctor", "patient", "date_time"]  # только 4 поля

    def get_doctor(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"

    def get_patient(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
