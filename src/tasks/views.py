from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from tasks.models import Task
from tasks.serializers import (
    TaskSerializer,
    AssigneeTaskSerializer,
    CommentTaskSerializer,
)


class TaskViewSet(viewsets.ModelViewSet):
    """Endpoint for working with tasks"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action == "assignee":
            return AssigneeTaskSerializer
        elif self.action == "comment":
            return CommentTaskSerializer
        else:
            return self.serializer_class

    @action(detail=True, methods=["patch"], url_path=r"assignee")
    def assignee(self, request, pk=None):
        """Add assignee to task."""
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task.assignee = serializer.data["assignee"]
        task.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path=r"complete")
    def complete(self, request, pk=None):
        """Mark task as completed."""
        task = self.get_object()
        task.is_completed = True
        task.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path=r"comment")
    def comment(self, request, pk=None):
        """Add comment to task."""
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task)
        return Response(serializer.data, status=status.HTTP_200_OK)
