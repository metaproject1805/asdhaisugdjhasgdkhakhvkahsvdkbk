from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from decimal import Decimal
from rest_framework import status
from ..models import Withdrawal
from .serializers import WithdrawalCreateSerializer
from base.utils.functions import create_user_notification
from rest_framework.exceptions import ValidationError



class CreateWithdrawalView(generics.CreateAPIView):
  serializer_class = WithdrawalCreateSerializer
  permission_classes = [IsAuthenticated]
  queryset = Withdrawal.objects.all()
  
  def post(self, *args, **kwargs):
    user = self.request.user
    data = self.request.data
    serializer = self.serializer_class(data=data)
    try:
      serializer.is_valid(raise_exception=True)
      amount = serializer._validated_data.get("amount")
      if amount is None:
        # raise ValidationError({"amount": "This field is required."})
        return Response("amount: This field is required.", status=status.HTTP_400_BAD_REQUEST)
      
      if int(amount) > user.balance:
        notification = create_user_notification(
          type="Info",
          title="Withdrawal Failed",
          message="Unfortunately, you do not have enough balance to complete your withdrawal. Please check your account and ensure you have sufficient funds."
        )
        user.notification.add(notification)
        user.save()
        return Response("you do not have enough balance. please try again later", status=status.HTTP_400_BAD_REQUEST)
      Withdrawal.objects.create(**serializer.validated_data, user=user)
      user.balance -= Decimal(int(amount))
      notification = create_user_notification(
        type="Info",
        title="Withdrawal Request Received",
        message="We have received your withdrawal request and it is currently being processed. Our team will review and approve it within 14 days."
      )
      user.notification.add(notification)
      user.save()
      return Response("withdrawal request received!", status=status.HTTP_200_OK)
    except ValidationError as e:
      return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)