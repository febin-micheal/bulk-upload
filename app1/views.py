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

    objs = []
    for row in worksheet.iter_rows(min_row=2):
        row_data = [str(cell.value) for cell in row]
        if not Grade.objects.filter(code=row_data[5]).exists():
            Grade.objects.create(code=row_data[5])
        grade = Grade.objects.filter(code=row_data[5]).values('id')
        if not Student.objects.filter(id=row_data[0]).exists():
            obj = Student(id=row_data[0], first_name=row_data[1], last_name=row_data[2], email=row_data[3], gender=row_data[4], grade_id=grade)
            objs.append(obj)

    Student.objects.bulk_create(objs)
    return redirect('list-view')

def list_view(request):
    object_list = list(Student.objects.all().values('id', 'first_name', 'last_name', 'email', 'gender', 'grade__code'))
    return render(request, 'list-view.html', {'object_list': object_list})
