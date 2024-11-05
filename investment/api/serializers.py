from rest_framework import serializers
from ..models import Investment

class InvestmentListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Investment
    fields = ["id", "duration", "price", "payment_slip", "payment_status", "days_remaining", "level"]
    

class InvestmentCreateSerializer(serializers.ModelSerializer):
  payment_slip = serializers.ImageField(use_url=True)
  class Meta:
    model = Investment
    fields = ["duration", "price", "payment_slip", "wallet_id", "wallet_email", "level"]
    
    
  def create(self, validated_data):
    instance = super().create(validated_data)
    return instance