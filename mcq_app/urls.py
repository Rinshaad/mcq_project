from django.urls import path
from .views import *

urlpatterns = [
    path('register/', user_registration, name='user-registration'),
    path('login/', user_login, name='user-login'),
    path('logout/', user_logout, name='user-logout'),
    path('add-question/', add_question, name='add-question'),
    path('questions/', question_list, name='student-questions'),
    path('answer-question/', answer_question, name='answer-question'),
    path('calculate-marks/', calculate_marks, name='calculate-marks'),

]