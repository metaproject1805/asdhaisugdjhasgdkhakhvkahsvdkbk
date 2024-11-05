from ..models import Profile, UserNotification
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from packages.models import Packages
from investment.api.serializers import InvestmentListSerializer
from withdrawals.models import Withdrawal
from withdrawals.api.serializers import WithdrawalListSerializer


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomUserDetailsSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username
        token['email'] = user.email
        token['active'] = user.phase_active
        token['is_superuser'] = user.is_superuser

        return token



class UserPassKeyPhaseActivateSerializer(serializers.Serializer):
  phase1 = serializers.CharField(max_length=15, required=True)
  phase2 = serializers.CharField(max_length=15, required=True)
  phase3 = serializers.CharField(max_length=15, required=True)
  phase4 = serializers.CharField(max_length=15, required=True)
  phase5 = serializers.CharField(max_length=15, required=True)
  phase6 = serializers.CharField(max_length=15, required=True)



class UserResetPasswordSerializer(serializers.Serializer):
  phase1 = serializers.CharField(max_length=15, required=True)
  phase2 = serializers.CharField(max_length=15, required=True)
  phase3 = serializers.CharField(max_length=15, required=True)
  phase4 = serializers.CharField(max_length=15, required=True)
  phase5 = serializers.CharField(max_length=15, required=True)
  phase6 = serializers.CharField(max_length=15, required=True)

  password = serializers.CharField(
    max_length=25,
    required=True,
    validators=[validate_password]
    )
  
  confirm_password = serializers.CharField(
    max_length=25,
    required=True,
    )
  
  def validate(self, data):
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    
    if password != confirm_password:
      raise serializers.ValidationError("Password do not match.")

    return data


class UserRegistrationSerializer(serializers.Serializer):
  ref_code = serializers.CharField(required=False, validators=[
          RegexValidator(
              regex=r'^[a-zA-Z0-9_]*$',
              message='invalid ref code',
          )
        ])
  email = serializers.EmailField(max_length=50, required=True)
  username = serializers.CharField(
    max_length=25, 
    required=True,
    validators=[
      RegexValidator(
              regex=r'^[a-zA-Z0-9_]*$',
              message='Username can only contain letters, numbers, and underscores.',
          )
    ]
    )
  password = serializers.CharField(
    max_length=25,
    required=True,
    validators=[validate_password]
    )
  
  confirm_password = serializers.CharField(
    max_length=25,
    required=True,
    )
  
  def validate(self, data):
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    
    if password != confirm_password:
      raise serializers.ValidationError("Password do not match.")

    return data

class PackageListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Packages
    fields = ["id", "level", "price", "payment_slip", "payment_status"]

class PackageLevelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Packages
    fields = ["level", "payment_status"]

  
  
class RefBySerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ["username"]

class ReferredProfileSerializer(serializers.ModelSerializer):
  active_package = PackageLevelSerializer(read_only=True)
  class Meta:
    model = Profile
    fields = ["username", "active", "active_package", "active"]


class ProfileNotificationSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserNotification
    fields = ["id", "type", "title", "message", "read"]



class ProfileSerializer(serializers.ModelSerializer):
  active_package = PackageListSerializer(read_only=True)
  referred = serializers.SerializerMethodField(read_only=True)
  withdrawals = serializers.SerializerMethodField(read_only=True)
  ref_by = RefBySerializer(read_only=True)
  notification = ProfileNotificationSerializer(many=True)
  investment = InvestmentListSerializer(read_only=True)
  class Meta:
    model = Profile
    fields = [
      "username", "ref_by", "email", "ref_code",
      "partnership_level", "active", "weekly_salary", "balance",
      "active_package", "referred", "investment_accumulation",
      "is_superuser", "ref_bonus", "notification", 
      "investment", "partnership_level", "withdrawals", "security_phase"
      ]
    
  
  def get_referred(self, obj):
    referred = Profile.objects.filter(ref_by=obj)    
    return ReferredProfileSerializer(referred, many=True).data

  def get_withdrawals(self, obj):
    withdrawals = Withdrawal.objects.filter(user=obj)
    return WithdrawalListSerializer(withdrawals, many=True).data