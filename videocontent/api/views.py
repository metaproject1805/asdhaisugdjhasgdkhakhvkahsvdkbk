from rest_framework.response import Response
from rest_framework import generics
from ..models import VideoContent
from .serializers import VideoContentListSerializer


class VideoContentList(generics.ListAPIView):
  serializer_class = VideoContentListSerializer
  queryset = VideoContent.objects.all().order_by("-pk")