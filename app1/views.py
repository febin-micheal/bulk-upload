from django.shortcuts import render, redirect
from .forms import UploadFileForm
import openpyxl
from .models import *
from django.contrib import messages

# Create your views here.

def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            if not excel_file.name.endswith('.xlsx'):
                messages.error(request, 'Please upload an excel file')
                return redirect('home')

            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb.active

            objs = list()
            for row in worksheet.iter_rows(min_row=2):
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                if not Student.objects.filter(id=row_data[0]).exists():
                    grade = Grade.objects.filter(code=row_data[5]).values('id')
                    obj = Student(id=row_data[0], first_name=row_data[1], last_name=row_data[2], email=row_data[3], gender=row_data[4], grade_id=grade)
                    objs.append(obj)

            Student.objects.bulk_create(objs)

            object_list = list(Student.objects.all().values('id', 'first_name', 'last_name', 'email', 'gender', 'grade__code'))
            return render(request, 'index.html', {'object_list': object_list})

    else:
        form = UploadFileForm()
    return render(request, 'home.html', {'form': form})
