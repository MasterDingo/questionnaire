# from django.db import models
from django.conf import settings
import json

# Create your models here.

_question_ids = []
_answer_ids = []

class Answer:
    __slots__ = ("id", "question_id", "text", "next")

    def __init__(self, question_id, text):
        self.question_id = question_id
        self.text = text
        self.next = None
        _answer_ids.append(self)
        self.id = len(_answer_ids)-1

    @classmethod
    def fromJson(cls, quest_id, json):
        text = json.get("text", None)

        if text:
            answer = cls(quest_id, text)
            next = json.get("next", None)
            if next:
                next_quest = Question.fromJson(next)
                answer.next = next_quest
            return answer
        else:
            return None

    @classmethod
    def byId(cls, id):
        if id < len(_answer_ids):
            return _answer_ids[id]
        else:
            return None


class Question:
    __slots__ = ("id", "text", "answers")

    def __init__(self, text):
        self.text = text
        self.answers = []
        _question_ids.append(self)
        self.id = len(_question_ids)-1

    def addAnswer(self, answer):
        self.answers.append(answer)

    @classmethod
    def fromJson(cls, json):
        quest_text = json.get("text", None)
        if(quest_text):
            quest = cls(quest_text)
            answers = []
            for answer_data in json.get("answers", []):
                quest.addAnswer(Answer.fromJson(quest.id, answer_data))

            return quest
        else:
            return None

    @classmethod
    def byId(cls, id):
        if id < len(_question_ids):
            return _question_ids[id]
        else:
            return None


with open(settings.JSON_FILE, "r") as f:
    data = json.load(f)

Question.fromJson(data)
