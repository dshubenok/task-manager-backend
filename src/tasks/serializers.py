from rest_framework import serializers

from tasks.models import Task, Comment


class CommentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'body']


class TaskSerializer(serializers.ModelSerializer):
    comments = CommentTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = [
            'is_completed',
            'assignee',
        ]


class AssigneeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "assignee",
        ]
