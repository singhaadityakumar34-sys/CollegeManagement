from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student


@login_required
def student_list(request):
    query = request.GET.get("q", "")
    course = request.GET.get("course", "")
    semester = request.GET.get("semester", "")
    gender = request.GET.get("gender", "")
    session = request.GET.get("session", "")

    students = Student.objects.all()

    if query:
        students = students.filter(
            name__icontains=query
        ) | students.filter(
            student_id__icontains=query
        ) | students.filter(
            email__icontains=query
        ) | students.filter(
            course__icontains=query
        )

    if course:
        students = students.filter(course=course)

    if semester:
        students = students.filter(semester=semester)

    if gender:
        students = students.filter(gender=gender)

    if session:
        students = students.filter(session=session)

    courses = Student.objects.values_list(
        "course", flat=True
    ).distinct()

    sessions = Student.objects.values_list(
        "session", flat=True
    ).distinct()

    return render(
        request,
        "students/student_list.html",
        {
            "students": students,
            "query": query,
            "courses": courses,
            "sessions": sessions,
            "selected_course": course,
            "selected_semester": semester,
            "selected_gender": gender,
            "selected_session": session,
        }
    )

@login_required
def add_student(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        course = request.POST.get("course")
        semester = request.POST.get("semester")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        date_of_birth = request.POST.get("date_of_birth")
        photo = request.FILES.get("photo")
        session = request.POST.get("session")

        if Student.objects.filter(student_id=student_id).exists():
            return render(
                request,
                "students/add_student.html",
                {"error": "Student ID already exists. Please use a different ID."}
            )

        if Student.objects.filter(email=email).exists():
            return render(
                request,
                "students/add_student.html",
                {"error": "Email already exists. Please use a different email."}
            )

        Student.objects.create(
            student_id=student_id,
            name=name,
            email=email,
            phone=phone,
            course=course,
            semester=semester,
            gender=gender,
            address=address,
            session=session,
            photo = photo,
            date_of_birth=date_of_birth
        )
        messages.success(request, "Student added successfully!")

        return redirect("student_list")

    return render(request, "students/add_student.html")

@login_required
def edit_student(request, student_id):
    student = Student.objects.get(student_id=student_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        course = request.POST.get("course")
        semester = request.POST.get("semester")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        date_of_birth = request.POST.get("date_of_birth")
        photo = request.FILES.get("photo")
        session = request.POST.get("session")

        if Student.objects.filter(email=email).exclude(
            student_id=student_id
        ).exists():
            return render(
                request,
                "students/edit_student.html",
                {
                    "student": student,
                    "error": "Email already exists. Please use a different email."
                }
            )

        student.name = name
        student.email = email
        student.phone = phone
        student.course = course
        student.semester = semester
        student.gender = gender
        student.address = address
        student.date_of_birth=date_of_birth
        student.session = session

        if photo:
            student.photo = photo
        student.save()
        messages.success(request, "Student updated successfully!")

        return redirect("student_list")

    return render(
        request,
        "students/edit_student.html",
        {"student": student}
    )

@login_required
def delete_student(request, student_id):
    student = Student.objects.get(student_id=student_id)
    student.delete()
    messages.success(request,"Student deleted successfully!")
    return redirect("student_list")

@login_required
def view_student(request, student_id):
    student = Student.objects.get(student_id=student_id)
    return render(request, "students/view_student.html", {"student": student})

@login_required
def dashboard(request):
    students = Student.objects.all()

    total_students = students.count()
    male_students = students.filter(gender="Male").count()
    female_students = students.filter(gender="Female").count()
    other_students = students.filter(gender="Other").count()

    total_courses = students.values("course").distinct().count()

    sessions = students.values_list("session", flat=True).distinct()

    return render(
        request,
        "students/dashboard.html",
        {
            "total_students": total_students,
            "male_students": male_students,
            "female_students": female_students,
            "other_students": other_students,
            "total_courses": total_courses,
            "sessions": sessions,
        }
    )