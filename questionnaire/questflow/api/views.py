from rest_framework import viewsets
from rest_framework.response import Response

import json

from .serializers import AnswerSerializer, QuestionSerializer
from ..models import Question, Answer


class QuestionnaireViewSet(viewsets.ViewSet):
    def get_question(self, request, question_id=None):
        sess = request.session
        if question_id is None:
            question_id = sess.get("question_id", 0)
        sess["question_id"] = question_id
        question = Question.byId(question_id)
        if "user_path" not in sess:
            sess["user_path"] = [question.text]
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def post_answer(self, request):
        sess = request.session
        data = json.loads(request.body)
        answer = Answer.byId(data.get("id"))
        sess["user_path"].append(answer.text)
        question = answer.next
        if question:
            sess["question_id"] = question.id
            if not question.answers:
                print("{}: {}".format(sess["user_path"][0], " -> ".join(sess["user_path"][1:])))
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        else:
            print("->".join(sess["user_path"]))
            return Response()


get_question = QuestionnaireViewSet.as_view({'get': 'get_question'})
post_answer = QuestionnaireViewSet.as_view({'post': 'post_answer'})
