from django.shortcuts import render, redirect
from .forms import UploadFileForm
import openpyxl
from .models import *
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']

            if not f.name.endswith('.xlsx'):
                messages.error(request, 'Please upload an excel file')
                return redirect('upload-file')

            with open('app1/uploads/excel.xlsx', 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

            return redirect('bulk-upload')
    else:
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})

def bulk_upload(request):
    excel_file = 'app1/uploads/excel.xlsx'

    wb = openpyxl.load_workbook(excel_file)
    worksheet = wb.active

    fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'grade_code']
    rows = [{field:str(cell.value) for field, cell in zip(fields, row)} for row in worksheet.iter_rows(min_row=2)]

    # reduce db hits in expense of loops
    grade_list =  list(Grade.objects.values()) # hit 1
    grade_codes = [grade['code'] for grade in grade_list]

    grades = [Grade(code=row['grade_code']) for row in rows if row['grade_code'] not in grade_codes]

    Grade.objects.bulk_create(grades) # hit 2
    grade_list =  list(Grade.objects.values()) # hit 3

    student_list =  list(Student.objects.values())  # hit 4    
    student_ids = [student['id'] for student in student_list]

    creates = []
    updates = []
    for row in rows:
        grade_id = [grade['id'] for grade in grade_list if grade['code'] == row['grade_code']]        
        student_id = int(row['id'])
        student = Student(id=student_id, first_name=row['first_name'], last_name=row['last_name'], email=row['email'], gender=row['gender'], grade_id=grade_id[0])
        if student_id in student_ids:
            updates.append(student)
        else:
            creates.append(student)

    if updates:
        Student.objects.bulk_update(updates, fields=['first_name', 'last_name', 'email', 'gender', 'grade_id']) # hit 5
    if creates:
        Student.objects.bulk_create(creates)   # hit 6
    return redirect('list-view')

def list_view(request):
    object_list = list(Student.objects.all().values('id', 'first_name', 'last_name', 'email', 'gender', 'grade__code'))
    return render(request, 'list-view.html', {'object_list': object_list})
