from django.shortcuts import render
from django.http import HttpResponse
from .models import Activity, Advisor, Campus, College, Course, Degree, Department
from .models import Exception, GPADeficiency, GPAStatus, GPAStatusQueryset
from .models import Requirement, Research, Requirement, Section, Student, Semester
from .models import Track
from django.contrib.auth.decorators import login_required
import yaml
import os
# Create your views here.

# def index(request):
#     my_dict = {'insert_me':"HELLO I AM FROM VIEWS.PY"}
#     return render(request, 'eh_app/index.html', context=my_dict)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_DIR = os.path.join(BASE_DIR, "eh_app", "fixtures", "test_seed.yaml")

def index(request):
    with open(SEED_DIR, 'r') as stream:
        try:
            data = yaml.load(stream)
            print(data)
        except yaml.YAMLError as exc:
            print(exc)

    students = Student.objects.filter()
    return render(request, 'eh_app/index.html', {'students': students})

def studentList(request):
    students = Student.objects.filter()
    return render(request, 'eh_app/student_list.html', {'students': students})
