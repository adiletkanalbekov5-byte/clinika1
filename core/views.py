from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render

from .models import User, Branch, DoctorProfile, PatientProfile, Appointment
from .serializers import (
    UserListSerializer, UserDetailSerializer,
    BranchListSerializer, BranchDetailSerializer,
    DoctorListSerializer, DoctorDetailSerializer,
    PatientListSerializer, PatientDetailSerializer,
    AppointmentListSerializer, AppointmentDetailSerializer
)
from .permissions import IsAdmin, IsDirector, IsDoctor, IsPatient

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
    filter_backends = [filters.SearchFilter]
    search_fields = ["username","first_name","last_name","email"]
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get","post","patch","put"]  # delete запрещён

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        return UserDetailSerializer

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        return Response(UserDetailSerializer(request.user).data)


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    permission_classes = [permissions.IsAuthenticated & (IsAdmin | IsDirector)]
    http_method_names = ["get","post","patch","put"]

    def get_serializer_class(self):
        if self.action == "list":
            return BranchListSerializer
        return BranchDetailSerializer


class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.select_related("user","branch").all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get","post","patch","put","delete"]

    def get_serializer_class(self):
        if self.action == "list":
            return DoctorListSerializer
        return DoctorDetailSerializer


class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.select_related("user").all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get","post","patch","put"]

    def get_serializer_class(self):
        if self.action == "list":
            return PatientListSerializer
        return PatientDetailSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related("doctor__user","patient__user","branch").all().order_by("-date_time")
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get","post","patch","put"]

    def get_serializer_class(self):
        if self.action == "list":
            return AppointmentListSerializer
        return AppointmentDetailSerializer

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_doctor():
            try:
                doctor = user.doctor_profile
                return qs.filter(doctor=doctor)
            except DoctorProfile.DoesNotExist:
                return Appointment.objects.none()
        if user.is_patient():
            try:
                patient = user.patient_profile
                return qs.filter(patient=patient)
            except PatientProfile.DoesNotExist:
                return Appointment.objects.none()
        return qs
