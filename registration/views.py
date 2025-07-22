
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Student, Enrollment
from django.contrib import messages
from django.http import JsonResponse


def home(request):
    return render(request, 'registration/home.html')

def student_panel(request):
    return render(request, 'registration/student_panel.html')

def admin_panel(request):
    return render(request, 'registration/admin_panel.html')

def create_course(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        name = request.POST.get('name')
        prerequisite_code = request.POST.get('prerequisite_code')
        
        # Check if the prerequisite exists
        prerequisite = Course.objects.filter(code=prerequisite_code).first() if prerequisite_code else None
        
        if prerequisite_code and not prerequisite:
            messages.error(request, 'Prerequisite course does not exist. Course not created.')
        else:
            # Create the course
            course = Course.objects.create(code=code, name=name, prerequisite=prerequisite)
            messages.success(request, f'Course "{course.name}" created successfully.')
        
    return render(request, 'registration/create_course.html')



def delete_course(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        course = Course.objects.filter(code=code).first() if code else None

        if course is not None:
            course.delete()
            messages.success(request, 'Course deleted successfully.')
        else:
            messages.error(request, 'Course does not exist.')

    return render(request, 'registration/delete_course.html')



def add_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        fees_paid = request.POST.get('fees_paid') == 'on' if 'fees_paid' in request.POST else False

        # Check if the student already exists
        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, f"A student with ID {student_id} already exists.")
        else:
            # If the student doesn't exist, create a new one
            Student.objects.create(student_id=student_id, name=name, fees_paid=fees_paid)
            messages.success(request, "Student added successfully.")

    return render(request, 'registration/add_student.html')



def display_all_courses(request):
    courses = Course.objects.all()
    return render(request, 'registration/display_all_courses.html', {'courses': courses})


def delete_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = Student.objects.filter(student_id=student_id).first()
        if student:
            student.delete()
            
    return render(request, 'registration/delete_student.html')


def display_all_students(request):
    students = Student.objects.all()
    return render(request, 'registration/display_all_students.html', {'students': students})




def enroll_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_code = request.POST.get('course_code')

        student = get_object_or_404(Student, student_id=student_id)
        course = get_object_or_404(Course, code=course_code)

        # Check if the student is already enrolled in the specific course
        already_enrolled = Enrollment.objects.filter(student=student, course=course).exists()

        if not student:
            return JsonResponse({'studentNotFound': True})
        elif not course:
            return JsonResponse({'courseNotFound': True})
        elif already_enrolled:
            return JsonResponse({'alreadyEnrolled': True})
        elif not student.fees_paid:
            return JsonResponse({'feeNotPaid': True})
        else:
            Enrollment.objects.create(student=student, course=course)
            return JsonResponse({'success': True})
    
    return render(request, 'registration/enroll_student.html')



def drop_registration(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_code = request.POST.get('course_code')
        student = Student.objects.filter(student_id=student_id).first()
        course = Course.objects.filter(code=course_code).first()
        if student and course:
            Enrollment.objects.filter(student=student, course=course).delete()
        
    return render(request, 'registration/drop_registration.html')



from django.core.exceptions import ObjectDoesNotExist

def display_enrolled_students(request):
    error_message = None
    enrolled_students = None

    if request.method == 'POST':
        course_code = request.POST.get('course_code')
        
        try:
            course = Course.objects.get(code=course_code)
            enrolled_students = Enrollment.objects.filter(course=course).values_list('student__student_id', 'student__name')

            if enrolled_students:
                return render(request, 'registration/display_enrolled_students.html', {'course_code': course_code, 'enrolled_students': enrolled_students})
                
        except ObjectDoesNotExist:
            error_message = 'No students enrolled in this course.'

    return render(request, 'registration/display_enrolled_students.html', {'error_message': error_message})



def display_enrolled_courses(request):
    error_message = None
    enrolled_courses = None
    student_name = None

    if request.method == 'POST':
        student_id = request.POST.get('student_id')

        try:
            student = Student.objects.get(student_id=student_id)
            enrolled_courses = Enrollment.objects.filter(student=student).values_list('course__code', 'course__name')
            student_name = student.name
            
            if enrolled_courses:
                return render(request, 'registration/display_enrolled_courses.html', {'student_id': student_id, 'student_name': student_name, 'enrolled_courses': enrolled_courses})
                
        except ObjectDoesNotExist:
            error_message = 'This student is not enrolled in any course or the student ID is invalid.'

    return render(request, 'registration/display_enrolled_courses.html', {'error_message': error_message})
