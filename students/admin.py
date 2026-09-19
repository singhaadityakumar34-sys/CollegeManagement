from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "name",
        "email",
        "phone",
        "course",
        "semester",
        "gender",
        "session",
    )
    search_fields = ("student_id","name","email")
    list_filter = ("course","semester","gender","session")