from rest_framework import serializers
from ..models import Withdrawal


class WithdrawalListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Withdrawal
    fields = ["id", "wallet_address", "payment_status", "amount"]


class AdminWithdrawalListSerializer(serializers.ModelSerializer):
  username = serializers.CharField(source='user.username', read_only=True)
  class Meta:
    model = Withdrawal
    fields = ["id", "wallet_address", "payment_status", "amount", "username"]


class WithdrawalCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Withdrawal
    fields = ["wallet_address", "amount"]