from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .serializers import InvestmentCreateSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from ..models import Investment
from base.utils.functions import create_user_notification
from base.functions import parse_querydict



class InvestmentCreateView(generics.CreateAPIView):
  serializer_class = InvestmentCreateSerializer
  queryset = Investment.objects.all()
  permission_classes = [IsAuthenticated]
  
  
  def create(self, request, *args, **kwargs):
    user = request.user
    data = parse_querydict(request.data)
    serializer = self.serializer_class(data=data)
    try:
      serializer.is_valid(raise_exception=True)
      if user.investment and user.investment.payment_status != "Inactive":
        notification = create_user_notification(title="Investment Purchase Failed", message="""
          Your investment purchase has failed because you have an active investment that hasn’t matured yet.
          """, type="Info")
        user.notification.add(notification)
        return Response({"message","you already have an active investment. please wait till it matures"}, status=HTTP_400_BAD_REQUEST)
        
      investment = serializer.save()
      investment.investment_manager()
      user.investment = investment
        
      notification = create_user_notification(title="Investment Created", message="""
        Congratulations! Your new investment investment has been successfully created with us. 
        We will review your submission and verify the details before approval. 
        Our team will reach out to you once the investment has been verified. 
        Thank you for choosing us.
        """, type="Success")
      user.notification.add(notification)
      user.save()
      return Response("Investment Created", status=HTTP_200_OK)
    except ValidationError as e:
      return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
      return Response({"message":str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)