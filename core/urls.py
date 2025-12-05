from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, BranchViewSet, DoctorProfileViewSet, PatientProfileViewSet, AppointmentViewSet, dashboard_admin, dashboard_director, dashboard_doctor, dashboard_patient
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"branches", BranchViewSet, basename="branches")
router.register(r"doctors", DoctorProfileViewSet, basename="doctors")
router.register(r"patients", PatientProfileViewSet, basename="patients")
router.register(r"appointments", AppointmentViewSet, basename="appointments")

urlpatterns = [
    # dashboards
    path("dash/admin/", dashboard_admin, name="dashboard_admin"),
    path("dash/director/", dashboard_director, name="dashboard_director"),
    path("dash/doctor/", dashboard_doctor, name="dashboard_doctor"),
    path("dash/patient/", dashboard_patient, name="dashboard_patient"),

    # api
    path("api/", include(router.urls)),

    # auth
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
