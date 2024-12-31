from rest_framework import generics
from ..models import Task
from .serializers import TaskListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q



class TaskListView(generics.ListAPIView):
  serializer_class = TaskListSerializer
  queryset = Task.objects.all().order_by("pk")
  permission_classes = [IsAuthenticated]
  
  def get_queryset(self, *args, **kwargs):
    user = self.request.user
    result_counter = user.active_package.max_number_of_task - user.video_watched_count
    watched_video_ids = user.video_watched.values_list('id', flat=True) 
    undone_task = Task.objects.filter(~Q(id__in=watched_video_ids)).order_by("?")[:result_counter]
    return undone_task
  
  
  
  
class SubmitTaskView(generics.RetrieveUpdateAPIView):
  serializers = TaskListSerializer
  queryset = Task.objects.all()
  permission_classes = [IsAuthenticated]
  lookup_field = "pk"
  
  
  def update(self, request, *args, **kwargs):
    user = request.user
    object = self.get_object()
    if  object is not None:
      if user.active_package and user.active_package.payment_status =="Active" and user.active_package.max_number_of_task > user.video_watched_count:        
        user.video_watched.add(object)
        user.video_watched_count += 1
        user.balance += user.active_package.earning_per_task
        user.save()
        return Response({"message","task submitted"}, status=status.HTTP_200_OK)
      return Response({"message":"You are either not eligible to perform this task or you have reach your daily task limit. Please buy a package or come back tomorrow."}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({"message","Task object not found. Please try again later"}, status=status.HTTP_404_NOT_FOUND)
  
  