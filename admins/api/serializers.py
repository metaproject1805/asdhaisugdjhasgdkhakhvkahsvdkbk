from profiles.models import Profile
from rest_framework import serializers
from packages.models import Packages
from profiles.api.serializers import ReferredProfileSerializer
from investment.models import Investment



class UserCountSerializer(serializers.Serializer):
  all_user = serializers.IntegerField()
  pending_approval = serializers.IntegerField()
  active_users = serializers.IntegerField()
  inactive_users = serializers.IntegerField()


class AdminPackageActionSerializer(serializers.Serializer):
  action_type = serializers.CharField(max_length=30)

class AdminInvestmentActionSerializer(serializers.Serializer):
  action_type = serializers.CharField(max_length=30)

class AdminWithdrawalActionSerializer(serializers.Serializer):
  action_type = serializers.CharField(max_length=30)
  

class AdminPackageListSerializer(serializers.ModelSerializer):
  payment_slip = serializers.ImageField(use_url=True)
  class Meta:
    model = Packages
    fields = ["id", "level", "price", "payment_slip", "payment_status", "wallet_id", "wallet_email"]


class AdminInvestmentListSerializer(serializers.ModelSerializer):
  payment_slip = serializers.ImageField(use_url=True)
  class Meta:
    model = Investment
    fields = ["id", "duration", "price", "payment_slip", "payment_status", "wallet_id", "wallet_email" ]


class AdminProfilePackageSerializer(serializers.ModelSerializer):
  active_package = AdminPackageListSerializer(read_only=True)
  class Meta:
    model = Profile
    fields = ["id","active_package", "username", "email"]

class AdminProfileInvestmentPackageSerializer(serializers.ModelSerializer):
  investment = AdminInvestmentListSerializer(read_only=True)
  class Meta:
    model = Profile
    fields = ["id", "username", "email", "investment"]
    
  
  def get_referred(self, obj):
    referred = Profile.objects.filter(ref_by=obj)    
    return ReferredProfileSerializer(referred, many=True).data
    
    