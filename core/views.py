from rest_framework import viewsets, permissions, filters
from django.shortcuts import render
from .models import User, Branch, DoctorProfile, PatientProfile, Appointment
from .serializers import (
    UserSerializer, UserListSerializer,
    BranchSerializer, BranchListSerializer,
    DoctorProfileSerializer, DoctorListSerializer,
    PatientProfileSerializer, PatientListSerializer,
    AppointmentSerializer, AppointmentListSerializer
)

# ---------- HTML dashboards ----------
def dashboard_admin(request):
    return render(request, "core/dashboard_admin.html")

def dashboard_director(request):
    return render(request, "core/dashboard_director.html")

def dashboard_doctor(request):
    return render(request, "core/dashboard_doctor.html")

def dashboard_patient(request):
    return render(request, "core/dashboard_patient.html")

# ---------- API ViewSets ----------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "first_name", "last_name", "email"]

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        return UserSerializer

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get","post","patch","put"]

    def get_serializer_class(self):
        if self.action == "list":
            return BranchListSerializer
        return BranchSerializer

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.select_related("user","branch").all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get","post","patch","put","delete"]

    def get_serializer_class(self):
        if self.action == "list":
            return DoctorListSerializer
        return DoctorProfileSerializer

class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.select_related("user").all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get","post","patch","put"]

    def get_serializer_class(self):
        if self.action == "list":
            return PatientListSerializer
        return PatientProfileSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related("doctor__user","patient__user","branch").all().order_by("-date_time")
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get","post","patch","put"]

    def get_serializer_class(self):
        if self.action == "list":
            return AppointmentListSerializer
        return AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if hasattr(user, "doctor_profile"):
            return qs.filter(doctor=user.doctor_profile)
        if hasattr(user, "patient_profile"):
            return qs.filter(patient=user.patient_profile)
        return qs
# core/views.py
from rest_framework import viewsets
from .models import PatientProfile
from .serializers import PatientListSerializer

