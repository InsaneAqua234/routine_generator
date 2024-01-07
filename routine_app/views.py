from django.shortcuts import render,redirect
from .schedule import Schedule
from .data import Courses, Resources
from .forms import DataEntryForm
import pandas as pd

def display_routine(request):
    '''routine_data = pd.read_excel("D:/Django try/routine_generator/routine_generator/routines.xlsx")'''
    return render(request, 'routine_app/success_page.html')

def show_routine(request):
    routine_data = pd.read_excel("D:/Django try/routine_generator/routine_generator/routines.xlsx", sheet_name=None)
    # Replace this with your actual routine generation logic

    return render(request, 'display_routine.html', {'routine_data': routine_data})
    '''return render(request, 'routine_app/generate_routine.html', {'routine_data': routine_data})'''

def data_upload(request):
    if request.method == 'POST':
        form = DataEntryForm(request.POST, request.FILES)
        if form.is_valid():
            # Read Excel file data into Pandas DataFrames
            faculty_data = request.FILES['faculty_file']
            courses_file = request.FILES['subject_file']
            section_data = request.FILES['section_file']
            room_data = request.FILES['room_file']
            routine_path = "D:/Django try/routine_generator/routine_generator/routines.xlsx"

            new_semester = Courses(courses_file)
            resource_data = Resources(teacher_data_file=faculty_data,
                              room_data_file=room_data,
                              section_data_file=section_data)

        resource_data.reset_resources()
        s = Schedule(new_semester, resource_data)
        s.create_classes()
        s.generate()
        s.display()
        s.save_schedule(routine_path)
        resource_data.update_resources()


            # Process the DataFrames as needed
            # Example: You can now directly use faculty_data, subject_data, and section_data in your logic

        return redirect(show_routine)  # Redirect to a success page
    else:
        form = DataEntryForm()

    return render(request, 'routine_app/data_entry.html', {'form': form})


def generate_routine(request):
    courses_file = "C:/Users/Shirso/Downloads/Code/Databases/course_data.xlsx"
    faculty_data = "C:/Users/Shirso/Downloads/Code/Databases/teacher_data.xlsx"
    room_data = "C:/Users/Shirso/Downloads/Code/Databases/room_data.xlsx"
    section_data = "C:/Users/Shirso/Downloads/Code/Databases/section_data.xlsx"
    routine_path = "D:/Django try/routine_generator/routine_generator/routines.xlsx"

    new_semester = Courses(courses_file)
    resource_data = Resources(teacher_data_file=faculty_data,
                              room_data_file=room_data,
                              section_data_file=section_data)

    resource_data.reset_resources()
    s = Schedule(new_semester, resource_data)
    s.create_classes()
    s.generate()
    s.display()
    s.save_schedule(routine_path)
    resource_data.update_resources()

    return render(request, 'routine_app/generate_routine.html', {'message': 'Routine generated successfully!'})

