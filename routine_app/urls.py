from django.urls import path
from .views import generate_routine, data_upload, display_routine, show_routine

urlpatterns = [
    path('generate_routine/', generate_routine, name='generate_routine'),
    path('data_entry/', data_upload, name='data_entry'),
    path('display_routine/', display_routine, name='display_routine'),
    path('show_routine/', show_routine, name='show_routine'),
    # Add more URLs as needed
]