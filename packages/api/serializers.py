from rest_framework import serializers
from ..models import Packages

class PackageListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Packages
    fields = ["id", "level", "price", "payment_slip", "payment_status", "days_remaining"]
    

class PackageCreateSerializer(serializers.ModelSerializer):
  payment_slip = serializers.ImageField(use_url=True)
  class Meta:
    model = Packages
    fields = ["level", "price", "payment_slip"]
    
    
  def create(self, validated_data):
    instance = super().create(validated_data)
    return instance
    