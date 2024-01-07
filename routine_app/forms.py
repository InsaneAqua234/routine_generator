from django import forms

class DataEntryForm(forms.Form):
    faculty_file = forms.FileField(label='Upload Faculty Details', required=True)
    subject_file = forms.FileField(label='Upload Subject Details', required=True)
    section_file = forms.FileField(label='Upload Section Details', required=True)
    room_file = forms.FileField(label='Uplodad Class-Room Details', required=True)