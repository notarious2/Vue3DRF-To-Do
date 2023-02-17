from django.shortcuts import render, get_object_or_404
from rest_framework.generics import GenericAPIView
from . import serializers
from .models import Task
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class TaskViewAPI(GenericAPIView):
    """An API to retrieve and create tasks"""

    serializer_class = serializers.TaskSerializer
    # queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all tasks of an authorized user"""
        tasks = Task.objects.filter(user=request.user)

        serializer = self.serializer_class(instance=tasks, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a task for registered user"""
        data = request.data
        serializer = self.serializer_class(data=data)
        user = request.user
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPI(GenericAPIView):
    """An API to update and delete individual tasks"""

    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    def patch(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        data = request.data
        serializer = self.serializer_class(task, data=data, partial=True)
        user = request.user

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(data="Task has been updated", status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskUpdatePriorityAPI(GenericAPIView):
    """Update priority of multiple tasks"""

    serializer_class = serializers.TaskPriorityUpdateSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        data = request.data
        # no need to make use of is_valid as it is tested during creation
        serializer = self.serializer_class(data=data)
        data = data["update"]

        # to make sure that all orders belong to a user
        user = request.user
        # filter tasks by user and date
        tasks = Task.objects.filter(pk__in=data).order_by("pk")
        tasks_with_user = Task.objects.filter(pk__in=data, user=user).order_by("pk")
        # to make sure that user is trying to modify own tasks
        if list(tasks) != list(tasks_with_user):
            return Response(
                "You cannot modify other users' tasks",
                status=status.HTTP_400_BAD_REQUEST,
            )

        for task in tasks:
            task.priority = data[str(task.task_id)]
            task.save()
        return Response(data="Tasks order has been updated", status=status.HTTP_200_OK)
