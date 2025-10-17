from django.contrib import admin
from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user", "position", "department", "hired_on")
    search_fields = ("user__username", "user__email", "position", "department")
