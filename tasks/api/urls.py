from django.urls import path
from .views import TaskListView, SubmitTaskView

urlpatterns = [
    path("task-list/", TaskListView.as_view(), name="task_list_view"),
    path("task-submit/<int:pk>/", SubmitTaskView.as_view(), name="task_submit_view")
]
