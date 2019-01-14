from django.urls import path
from .views import questions

urlpatterns = [
    path('question/', questions),
    path('question/<int:question_id>/', questions)
]
