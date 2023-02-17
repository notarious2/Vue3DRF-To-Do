from django.urls import path
from .views import TaskViewAPI, TaskDetailAPI, TaskUpdatePriorityAPI

urlpatterns = [
    path("", TaskViewAPI.as_view(), name="get_tasks"),
    path("<uuid:task_id>", TaskDetailAPI.as_view(), name="change_tasks"),
    path("update/order", TaskUpdatePriorityAPI.as_view(), name="update_priority"),
]
