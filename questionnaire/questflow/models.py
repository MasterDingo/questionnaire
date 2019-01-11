# from django.db import models

# Create your models here.

__question_ids = []
__answer_ids = []

class Answer:
    __slots__ = ("id", "question_id", "text", "next")

    def __init__(self, question_id, text):
        self.question_id = question_id
        self.text = text
        self.next = None
        __answer_ids.append(self)
        self.id = len(__answer_ids)-1

    @classmethod
    def fromJson(cls, json):
        text = json.get("text", None)

        if text:
            answer = cls(text)
            next = json.get("next", None)
            if next:
                next_quest = Question.fromJson(next)
                answer.next = next_quest
            return answer
        else:
            return None

    @classmethod
    def byId(cls, id):
        if id < len(__answer_ids):
            return __answer_ids[id]
        else:
            return None


class Question:
    __slots__ = ("id", "text", "answers")

    def __init__(self, text):
        self.text = text
        self.answers = []
        __question_ids.append(self)
        self.id = len(__question_ids)-1

    def addAnswer(self, answer):
        self.answers.append(answer)

    @classmethod
    def fromJson(cls, json):
        quest_text = json.get("text", None)
        if(quest_text):
            quest = cls(quest_text)
            answers = []
            for answer_data in json.get("answers", []):
                quest.addAnswer(Answer.fromJson(answer_data))

            return quest
        else:
            return None

    @classmethod
    def byId(cls, id):
        if id < len(__question_ids):
            return __question_ids[id]
        else:
            return None
