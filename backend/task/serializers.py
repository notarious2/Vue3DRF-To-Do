from rest_framework import serializers, status
from .models import Task
from uuid import UUID
from rest_framework.response import Response


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("task_id", "date", "priority", "text", "completed")


class TaskPriorityUpdateSerializer(serializers.Serializer):
    """Custom serializer for updating priorities of tasks"""

    update = serializers.DictField(child=serializers.IntegerField(), allow_empty=False)

    def __init__(self, *args, **kwargs):
        """To check that uuid compatible string is passed as a key"""
        # to avoid problems with swagger
        if "data" in kwargs:
            priority_dict = kwargs["data"]["update"]
            for key, value in priority_dict.items():
                try:
                    UUID(key, version=4)
                except:
                    raise serializers.ValidationError(
                        "task_id is not a valid uuid field"
                    )
                try:
                    if isinstance(value, (bool, float, str)):
                        raise Exception
                    elif int(value) <= 0:
                        raise Exception
                except:
                    raise serializers.ValidationError("priority is not a valid integer")

        return super(TaskPriorityUpdateSerializer, self).__init__(*args, **kwargs)
