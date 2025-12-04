from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from .models import User, Branch, DoctorProfile, PatientProfile, Appointment
from .serializers import UserSerializer, BranchSerializer, DoctorProfileSerializer, PatientProfileSerializer, AppointmentSerializer
from .permissions import IsAdmin, IsDirector, IsDoctor, IsPatient

# ---------- Template dashboards (very simple) ----------
def dashboard_admin(request):
    return render(request, "core/dashboard_admin.html")

def dashboard_director(request):
    return render(request, "core/dashboard_director.html")

def dashboard_doctor(request):
    return render(request, "core/dashboard_doctor.html")

def dashboard_patient(request):
    return render(request, "core/dashboard_patient.html")

# ---------- API ViewSets ----------
class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated & (IsAdmin | IsDirector)]
    http_method_names = ['get', 'post', 'put', 'patch']
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "first_name", "last_name", "email"]
    http_method_names = ['get', 'post', 'put', 'patch']
    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        return Response(UserSerializer(request.user).data)

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.select_related("user", "branch").all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch']
class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.select_related("user").all()
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch']
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related("doctor__user","patient__user","branch").all().order_by("-date_time")
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_doctor():
            # врач видит только свои записи
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
        # директор и админ видят всё
        return qs
