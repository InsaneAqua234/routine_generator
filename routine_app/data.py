import pandas as pd


class Courses:
    class Section:
        title = ""
        courses = None
        total_slots=30

        def __init__(self, title, courses_df):
            self.title = title
            self.courses = courses_df
            self.courses.columns=self.courses.columns.str.replace(' ', '_')
            self.courses.set_index(["SUBJECT_CODE"])
            self.courses["UNALLOCATED"]=self.courses["HOUR"]
            #print(self.courses)

        def get_title(self):
            return self.title

        def get_courses(self):
            return self.courses

        def get_total_slots(self):
            return self.total_slots

    def __init__(self, course_data_file):
        with pd.ExcelFile(course_data_file) as file:
            sections_title = file.sheet_names

        self.sections = []
        for i in sections_title:
            df = pd.read_excel(course_data_file, i)
            new_section = self.Section(i, df)
            self.sections.append(new_section)

    def get_sections(self):
        return self.sections

class Resources:
    def __init__(self,teacher_data_file,room_data_file,section_data_file):
        self.teacher_data_file=teacher_data_file
        self.room_data_file=room_data_file
        self.section_data_file=section_data_file

        self.Faculty_data = pd.read_excel(self.teacher_data_file)
        self.Faculty_data.columns = self.Faculty_data.columns.str.replace(' ', '_')
        self.Faculty_data.rename(columns={'FACULTY_ID':'RESOURCE_ID'},inplace=True)

        self.Room_data = pd.read_excel(self.room_data_file)
        self.Room_data.columns = self.Room_data.columns.str.replace(' ', '_')
        self.Room_data.rename(columns={'ROOM_NO': 'RESOURCE_ID'}, inplace=True)

        self.Section_data = pd.read_excel(self.section_data_file)
        self.Section_data.columns = self.Section_data.columns.str.replace(' ', '_')
        self.Section_data.rename(columns={'SECTION_TITLE': 'RESOURCE_ID'}, inplace=True)

    def update_resources(self):
        self.Room_data.rename(columns={'RESOURCE_ID': 'ROOM_NO'}, inplace=True)
        self.Faculty_data.rename(columns={'RESOURCE_ID': 'FACULTY_ID'}, inplace=True)
        self.Section_data.rename(columns={'RESOURCE_ID': 'SECTION_TITLE'}, inplace=True)

        self.Room_data.to_excel(self.room_data_file,index=False)
        self.Faculty_data.to_excel(self.teacher_data_file, index=False)
        self.Section_data.to_excel(self.section_data_file, index=False)

    def reset_resources(self):
        self.Faculty_data['SLOT_AVAILIBILITY']='0.0.0.0.0'
        self.Room_data['SLOT_AVAILIBILITY']='0.0.0.0.0'
        self.Section_data['SLOT_AVAILIBILITY']='0.0.0.0.0'


# data=Courses("..\\Databases\\course_data.xlsx")
# resource_data=Resources("..\\Databases\\teacher_data.xlsx","..\\Databases\\room_data.xlsx","..\\Databases\\section_data.xlsx")

