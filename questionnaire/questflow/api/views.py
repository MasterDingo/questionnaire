from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import AnswerSerializer, QuestionSerializer
from .models import Question, Answer


class QuestionnaireViewSet(viewsets.ViewSet):
    def get_question(self, request, question_id=0):
        question = Question.byId(question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def post_answer(self, request):
        pass


get_question = QuestionnaireViewSet.as_view({'get': 'get_question'})
post_answer = QuestionnaireViewSet.as_view({'post': 'post_answer'})
