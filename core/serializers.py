from rest_framework import serializers
from .models import User, Branch, DoctorProfile, PatientProfile, Appointment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role"]

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=User.ROLE_DOCTOR), source="user", write_only=True)

    class Meta:
        model = DoctorProfile
        fields = ["id", "user", "user_id", "branch", "specialization"]

class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=User.ROLE_PATIENT), source="user", write_only=True)

    class Meta:
        model = PatientProfile
        fields = ["id", "user", "user_id", "phone", "birthdate"]

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=DoctorProfile.objects.all(), source="doctor", write_only=True)
    patient = PatientProfileSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=PatientProfile.objects.all(), source="patient", write_only=True)
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), source="branch", write_only=True, allow_null=True, required=False)

    class Meta:
        model = Appointment
        fields = ["id", "doctor", "doctor_id", "patient", "patient_id", "branch","branch_id", "date_time", "status", "notes", "created_at"]
