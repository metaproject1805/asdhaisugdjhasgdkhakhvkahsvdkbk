from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from profiles.models import Profile
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from .serializers import AdminProfilePackageSerializer, AdminPackageActionSerializer, UserCountSerializer, AdminProfileInvestmentPackageSerializer, AdminInvestmentActionSerializer, AdminWithdrawalActionSerializer
from django.db.models import Count, Case, When, IntegerField, Q
from base.utils.permissions import IsAdminUser
from base.utils.functions import remove_five_percent, create_user_notification
from rest_framework.exceptions import ValidationError
from withdrawals.models import Withdrawal
from withdrawals.api.serializers import AdminWithdrawalListSerializer
from profiles.models import Profile
from profiles.api.serializers import ProfileSerializer


class UserCountView(APIView):
  serializer_class = UserCountSerializer
  permission_classes = [IsAdminUser]
  
  def get(self, *args, **kwargs):
    users = Profile.objects.aggregate(
        total_users=Count('id'),
        pending_users=Count(Case(When(Q(active_package__payment_status='Pending') | Q(investment__payment_status='Pending'), then=1), output_field=IntegerField())),
        active_users=Count(Case(When(Q(active_package__payment_status='Active') | Q(investment__payment_status="Active"), then=1), output_field=IntegerField())),
        inactive_users=Count(Case(
          When(
            Q(active_package__isnull=True) | 
            Q(investment__isnull=True) &
            Q(active_package__payment_status='Inactive') | 
            Q(investment__payment_status='Inactive'), 
            then=1
          ), 
          output_field=IntegerField()
        ))
    )

    serializer = UserCountSerializer({
      "all_user": users["total_users"],
      "pending_approval": users["pending_users"],
      "active_users": users["active_users"],
      "inactive_users": users["inactive_users"]
      })
    return Response(serializer.data, status=HTTP_200_OK)


class AllUserView(generics.ListAPIView):
  serializer_class = AdminProfilePackageSerializer
  permission_classes = [IsAdminUser]
  queryset = Profile.objects.all().order_by("-pk")


class DailyInvestmentUpdate(APIView):
  serializer_class = ProfileSerializer
  # permission_classes = [IsAdminUser]
  # queryset = Profile.objects.filter(investment__payment_status="Active")

  def get(self, *args, **kwargs):
    users_with_an_active_investment = Profile.objects.filter(investment__payment_status="Active")
    for user in users_with_an_active_investment:
      if user.investment.days_remaining <= 0:
        user.balance += user.investment.price
        user_notification=create_user_notification(
          type="Success", 
          title="Package Expiration Notice", 
          message="""
          Your investment package has expired. Your capital has been added to your balance, and the investment package has been deleted.
          you can now withdraw your capital. Thank you
          """
          )
        user.notification.add(user_notification)
        user.investment.delete()
        user.investment = None
        user.save()
        
      else:
        user.investment.days_remaining -= 1
        if user.investment.level == 2:
          user.balance += 1
        else:
          daily_earning_percentage = user.investment.daily_earning / 100
          adding_up = daily_earning_percentage * user.investment.price
          user.balance += adding_up
        user.investment.save()
        user.save()
    return Response("Investment Updated", status=200)

class DailyUserUpdate(APIView):
  serializer_class = ProfileSerializer
  # permission_classes = [IsAdminUser]
  # queryset = Profile.objects.filter(investment__payment_status="Active")

  def get(self, *args, **kwargs):
    users_with_an_active_package = Profile.objects.filter(active_package__payment_status="Active")
    for user in users_with_an_active_package:
      if user.active_package.days_remaining <= 0:
        user.balance += user.active_package.price
        user_notification=create_user_notification(
          type="Success", 
          title="Package Expiration Notice", 
          message="""
          Your investment package has expired. Your capital has been added to your balance, and the investment package has been deleted.
          you can now withdraw your capital. Thank you
          """
          )
        user.notification.add(user_notification)
        user.active_package.delete()
        user.active_package = None
        user.save()
        
      else:
        user.active_package.days_remaining -= 1
        user.video_watched_count = 0
        user.video_watched.clear()
        user.active_package.save()
        user.save()
    return Response("User Updated", status=200)


class AllWithdrawalView(generics.ListAPIView):
  serializer_class = AdminWithdrawalListSerializer
  permission_classes = [IsAdminUser]
  queryset = Withdrawal.objects.filter(payment_status="Pending").order_by("-pk")

class PendingUserView(generics.ListAPIView):
  serializer_class = AdminProfilePackageSerializer
  permission_classes = [IsAdminUser]
  queryset = Profile.objects.filter(active_package__payment_status="Pending").order_by("-pk")


class PendingInvestmentUserView(generics.ListAPIView):
  serializer_class = AdminProfileInvestmentPackageSerializer
  permission_classes = [IsAdminUser]
  queryset = Profile.objects.filter(investment__payment_status="Pending").order_by("-pk")

class InactiveUserView(generics.ListAPIView):
  serializer_class = AdminProfilePackageSerializer
  permission_classes = [IsAdminUser]
  queryset = Profile.objects.filter(
    Q(active_package__isnull=True) | 
    Q(investment__isnull=True) &
    Q(active_package__payment_status="Inactive") |
    Q(investment__payment_status="Inactive")
    ).order_by("-pk")

class ActiveUserView(generics.ListAPIView):
  serializer_class = AdminProfilePackageSerializer
  permission_classes = [IsAdminUser]
  queryset = Profile.objects.filter(Q(active_package__payment_status="Active")| Q(investment__payment_status="Active")).order_by("-pk")


class PendingUserPackagesView(generics.ListAPIView):
  serializer_class = AdminProfilePackageSerializer
  permission_classes = [IsAdminUser]
  queryset = Profile.objects.all().order_by("-pk")
  


class AdminPackageActionView(APIView):
  serializer_class = AdminPackageActionSerializer
  lookup_fields = "pk"
  queryset = Profile.objects.all()
  permission_classes = [IsAdminUser]
  
  def put(self, request, *args, **kwargs):
    pk = kwargs.get("pk")
    data = request.data
    serializer = self.serializer_class(data=data)
    try:
      serializer.is_valid(raise_exception=True)
      action_type = serializer.validated_data.get("action_type")
      instance  = get_object_or_404(Profile, pk=pk)
      if action_type == "approve":
        if instance.active_package:
          active_package = instance.active_package
          active_package.payment_status = "Active"
          instance.active = True
          if instance.ref_by: 
            instance.ref_by.balance += remove_five_percent(active_package.price)
            if instance.ref_by.pending_ref.filter(id=instance.id).exists():
              instance.ref_by.pending_ref.remove(instance)
            if not instance.ref_by.active_ref.filter(id=instance.id).exists():
              instance.active_ref.add(instance)
            ref_notification = create_user_notification(title="Great News About Your Referral!", message=f"""
                We’re thrilled to inform you that your referral, {instance.username}, has successfully activated their account and investment package!
                Thank you for spreading the word about us. 
                Your support makes a difference, and we appreciate your efforts in growing our community.
                As a token of our appreciation, we’ve credited your account with a referral bonus.
                Thank you
                """)
            instance.ref_by.notification.add(ref_notification)
            instance.ref_by.save()
          notification = create_user_notification(title="Package Approved!", message="""
              Great news! Your investment package has been successfully approved and will last for 90 days. 
              We appreciate your trust in us and are excited to support you on your investment journey.
              """)
          instance.notification.add(notification)

          active_package.save()
          instance.save()
          return Response({"message","approved"}, status=HTTP_200_OK)
        return Response("Please select a package and try again", status=HTTP_400_BAD_REQUEST)
      elif action_type == "reject":
        if instance.active_package:
          instance.active_package=None
          notification = create_user_notification(title="Package Not Approved!", message="""
              Thank you for your submission. 
              Unfortunately, your investment package has not been approved at this time. 
              This may be due to certain criteria that were not met during our review process. 
              We encourage you to review your submission and make any necessary adjustments.
              """, type="Info")
          instance.notification.add(notification)
          instance.save()
        return Response({"message","rejected"}, status=HTTP_200_OK)
      else:
        return Response("invalid action provided. either star or moon expected", status=HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return Response({"message",serializer.errors}, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message",str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
      
      



class AdminInvestmentActionView(APIView):
  serializer_class = AdminInvestmentActionSerializer
  lookup_fields = "pk"
  queryset = Profile.objects.all()
  permission_classes = [IsAdminUser]
  
  def put(self, request, *args, **kwargs):
    pk = kwargs.get("pk")
    data = request.data
    serializer = self.serializer_class(data=data)
    try:
      serializer.is_valid(raise_exception=True)
      action_type = serializer.validated_data.get("action_type")
      instance  = get_object_or_404(Profile, pk=pk)
      if action_type == "approve":
        investment = instance.investment
        if investment:
          investment.payment_status = "Active"
          instance.active = True
          if instance.ref_by:
            instance.ref_by.balance += remove_five_percent(investment.price)
            if instance.ref_by.pending_ref.filter(id=instance.id).exists():
              instance.ref_by.pending_ref.remove(instance)
            if not instance.ref_by.active_ref.filter(id=instance.id).exists():
              instance.active_ref.add(instance)
            ref_notification = create_user_notification(title="Great News About Your Referral!", message=f"""
                We’re thrilled to inform you that your referral, {instance.username}, has successfully activated their account and investment package!
                Thank you for spreading the word about us. 
                Your support makes a difference, and we appreciate your efforts in growing our community.
                As a token of our appreciation, we’ve credited your account with a referral bonus.
                Thank you
                """)
            instance.ref_by.notification.add(ref_notification)
            instance.ref_by.save()
          notification = create_user_notification(title="Investment Approved!", message=f"""
              Great news! Your investment package has been successfully approved and will last for {instance.investment.days_remaining} days. 
              We appreciate your trust in us and are excited to support you on your investment journey.
              """)
          instance.notification.add(notification)
          investment.save()
          instance.save()
          return Response({"message","approved"}, status=HTTP_200_OK)
        return Response("Please select a package and try again", status=HTTP_400_BAD_REQUEST)
      elif action_type == "reject":
        if instance.investment:
          instance.investment=None
          notification = create_user_notification(title="Investment Not Approved!", message="""
              Thank you for your submission. 
              Unfortunately, your investment package has not been approved at this time. 
              This may be due to certain criteria that were not met during our review process. 
              We encourage you to review your submission and make any necessary adjustments.
              """, type="Info")
          instance.notification.add(notification)
          instance.save()
        return Response({"message","rejected"}, status=HTTP_200_OK)
      else:
        return Response("invalid action provided. either star or moon expected", status=HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return Response({"message",serializer.errors}, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message",str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
      
      



class AdminWithdrawalActionView(APIView):
  serializer_class = AdminWithdrawalActionSerializer
  lookup_fields = "pk"
  queryset = Withdrawal.objects.all()
  permission_classes = [IsAdminUser]
  
  def put(self, request, *args, **kwargs):
    pk = kwargs.get("pk")
    data = request.data
    serializer = self.serializer_class(data=data)
    try:
      serializer.is_valid(raise_exception=True)
      action_type = serializer.validated_data.get("action_type")
      instance  = get_object_or_404(Withdrawal, pk=pk)
      if action_type == "approve":
        instance.payment_status = "Approved"
        notification = create_user_notification(
          type="Success",
          title="Withdrawal Request Approved",
          message="Your withdrawal request has been approved! The funds have been successfully paid to the address you provided."
        )
        instance.user.notification.add(notification)
        instance.user.save()
        instance.save()
        return Response({"message":"withdrawal approved!!"}, status=HTTP_200_OK)
      elif action_type == "reject":
        instance.payment_status = "Rejected"
        instance.user.balance += instance.amount
        notification = create_user_notification(
          type="Info",
          title="Withdrawal Request Rejected",
          message="We regret to inform you that your withdrawal request has been rejected. Your funds have been returned to your balance. Please check your account details and try again."
        )
        instance.user.notification.add(notification)
        instance.user.save()
        instance.save()
        return Response({"message","withdrawal rejected!!"}, status=HTTP_200_OK)
      else:
        return Response("invalid action provided. either star or moon expected", status=HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return Response({"message",serializer.errors}, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message",str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)