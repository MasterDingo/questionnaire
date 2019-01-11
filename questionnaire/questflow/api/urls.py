from django.urls import path
from .views import get_question, post_answer

urlpatterns = [
    path('question/', get_question),
    path('question/<question_id>/', post_answer),
]
