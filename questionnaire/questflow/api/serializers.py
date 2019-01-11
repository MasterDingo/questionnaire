from rest_framework import serializers


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    answers = AnswerSerializer()
