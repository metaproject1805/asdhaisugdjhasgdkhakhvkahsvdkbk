from rest_framework import serializers
from ..models import VideoContent

class VideoContentListSerializer(serializers.Serializer):
  class Meta:
    model = VideoContent
    fields=["id","category", "video"]