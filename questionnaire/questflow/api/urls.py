from django.urls import path
from .views import get_question, post_answer

urlpatterns = [
    path('question/', get_question),
    path('answer/', post_answer),
]
