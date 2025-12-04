from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"branches", views.BranchViewSet, basename="branch")
router.register(r"doctors", views.DoctorProfileViewSet, basename="doctor")
router.register(r"patients", views.PatientProfileViewSet, basename="patient")
router.register(r"appointments", views.AppointmentViewSet, basename="appointment")

urlpatterns = [
    # HTML dashboards
    path("dash/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("dash/director/", views.dashboard_director, name="dashboard_director"),
    path("dash/doctor/", views.dashboard_doctor, name="dashboard_doctor"),
    path("dash/patient/", views.dashboard_patient, name="dashboard_patient"),

    # API
    path("api/", include(router.urls)),
    # auth tokens
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
