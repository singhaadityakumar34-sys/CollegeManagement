from django.db import models
from django.utils import timezone

class Student(models.Model):
    student_id = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    semester = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    photo = models.ImageField(upload_to="student_photos/", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    registration_date = models.DateField(default=timezone.now)
    session = models.CharField(max_length=20,default="2025-2029")

    def __str__(self):
        return self.name