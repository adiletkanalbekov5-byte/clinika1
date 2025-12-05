from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Branch, DoctorProfile, PatientProfile, Appointment

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff", "is_active")

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone")

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "specialization", "branch")

from django.contrib import admin
from .models import PatientProfile

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "get_phone", "get_birthdate", "user")

    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = "Телефон"

    def get_birthdate(self, obj):
        return obj.user.birthdate
    get_birthdate.short_description = "Дата рождения"

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("date_time", "doctor", "patient", "status", "branch")
    list_filter = ("status", "branch", "date_time")
