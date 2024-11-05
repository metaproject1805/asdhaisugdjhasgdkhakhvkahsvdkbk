from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import PaymentSerializer
from ..models import Payment


class PaymentListCreateView(generics.ListCreateAPIView):
  serializer_class = PaymentSerializer
  queryset = Payment.objects.all().order_by("-pk")
  