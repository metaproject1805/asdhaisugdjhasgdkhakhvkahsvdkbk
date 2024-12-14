from .serializers import ProfileSerializer, UserRegistrationSerializer, UserPassKeyPhaseActivateSerializer, UserResetPasswordSerializer, ProfileNotificationSerializer
from ..models import Profile, UserNotification
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .validations import UserModel, custom_user_validation
from rest_framework.views import APIView
from rest_framework.response import Response
from base.utils.functions import generate_phase_code, create_user_notification
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken



class ReadUserNotification(generics.RetrieveAPIView):
  serializer_class = ProfileNotificationSerializer
  lookup_field = "pk"
  queryset = UserNotification.objects.all()
  
  def put(self, request, *args, **kwargs):
    object = self.get_object()
    object.read = True
    object.save()
    return Response({"message":"notification read"}, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
  serializer_class = UserRegistrationSerializer
  
  def post(self, request, *args, **kwargs):
    clean_data = custom_user_validation(request.data)
    serializer = self.serializer_class(data=clean_data)
    try:
      serializer.is_valid(raise_exception=True)
      clean_ref_code = serializer.validated_data.get("ref_code")
      username = serializer.validated_data.get("username").lower()
      serializer.validated_data.pop("confirm_password")
      serializer.validated_data.pop("username")
      security_phase_1 = generate_phase_code()
      security_phase_2 = generate_phase_code()
      security_phase_3 = generate_phase_code()
      security_phase_4 = generate_phase_code()
      security_phase_5 = generate_phase_code()
      security_phase_6 = generate_phase_code()
      security_phase = f"{security_phase_1} {security_phase_2} {security_phase_3} {security_phase_4} {security_phase_5} {security_phase_6}"
      user = UserModel.objects.create_user(**serializer.validated_data,
                                username = username,
                                balance = 20.00,
                                security_phase = security_phase,
                                ) 
      notification = create_user_notification(title="Welcome to Our Community!", message=f"""
            Dear {user.username},
            Welcome to Metatask! We’re excited to have you join our community. To get you started, we’ve credited your account with 20 points as a signup bonus. 🎁
            Welcome aboard! We’re thrilled to have you join our community. As a new member, you’ll have access to a range of features and resources designed to help you succeed financially. 
            Thank you for choosing us, and we look forward to helping you achieve your goals!
            Best regards,
            The Metatask Team
        """)
      user.notification.add(notification)
      if(clean_ref_code):
          up_line = get_object_or_404(Profile, username=clean_ref_code)
          user.ref_by = up_line
          up_line.pending_ref.add(user)
          notification = create_user_notification(title="Thank You for Your Referral!", message=f"""
              We’re excited to let you know that your referral, {user.username}, has joined our community!
              Your support helps us grow and enables us to provide even better services to all our users.
              As a token of our appreciation, keep an eye out for your rewards coming soon!
              If you have any questions or need assistance, feel free to reach out.
            """)
          up_line.notification.add(notification)
          up_line.save()
      user.save()
      
      return Response({"message":user.security_phase}, status=status.HTTP_200_OK)
    except ValidationError as  e:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as  e:
      return Response(str(e), status=500)
      
  


class SuperUserRegistrationView(APIView):
  serializer_class = UserRegistrationSerializer
  
  def post(self, request, *args, **kwargs):
    clean_data = custom_user_validation(request.data)
    serializer = self.serializer_class(data=clean_data)
    try:
      serializer.is_valid(raise_exception=True)
      clean_ref_code = serializer.validated_data.get("ref_code")
      username = serializer.validated_data.get("username").lower()
      serializer.validated_data.pop("confirm_password")
      serializer.validated_data.pop("username")
      security_phase_1 = generate_phase_code()
      security_phase_2 = generate_phase_code()
      security_phase_3 = generate_phase_code()
      security_phase_4 = generate_phase_code()
      security_phase_5 = generate_phase_code()
      security_phase_6 = generate_phase_code()
      security_phase = f"{security_phase_1} {security_phase_2} {security_phase_3} {security_phase_4} {security_phase_5} {security_phase_6}"
      user = UserModel.objects.create_superuser(**serializer.validated_data,
                                username = username,
                                security_phase = security_phase,
                                )
      notification = create_user_notification(title="Welcome to Our Community!", message=f"""
            Dear {user.username},
            Welcome aboard! We’re thrilled to have you join our community. 
            As a new member, you’ll have access to a range of features and resources designed to help you succeed financially. 
            Whether you’re here to invest, learn, or connect, we’re committed to supporting you every step of the way.
            If you have any questions or need assistance, don’t hesitate to reach out to our support team. 
            Thank you for choosing us, and we look forward to helping you achieve your goals!
            Best regards,
            The Metatask Team
        """)
      user.notification.add(notification)
      if(clean_ref_code):
          up_line = get_object_or_404(Profile, username=clean_ref_code)
          user.ref_by = up_line
          up_line.pending_ref.add(user)
          notification = create_user_notification(title="Thank You for Your Referral!", message=f"""
              We’re excited to let you know that your referral, {user.username}, has joined our community!
              Your support helps us grow and enables us to provide even better services to all our users.
              As a token of our appreciation, keep an eye out for your rewards coming soon!
              If you have any questions or need assistance, feel free to reach out.
            """)
          up_line.notification.add(notification)
          up_line.save()
      user.save()
      
      return Response({"message":user.security_phase}, status=status.HTTP_200_OK)
    except ValidationError as  e:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as  e:
      return Response(str(e), status=500)
      
  


class UserDetailView(generics.RetrieveAPIView):
  serializer_class = ProfileSerializer
  lookup_field = 'pk'
  queryset = Profile.objects.all()
  permission_classes = [IsAuthenticated]
  
  

class PassKeyPhaseActivateView(APIView):
  serializer_class = UserPassKeyPhaseActivateSerializer
  permission_classes = [IsAuthenticated]
  
  def post(self, request, *args, **kwargs):
    user = request.user
    data = request.data
    serializer = self.serializer_class(data=data)
    try:
      serializer.is_valid(raise_exception=True)
      validated_data = serializer.validated_data
      user_security_phase = user.security_phase.split(' ')
      user_phase_1 = user_security_phase[0]
      user_phase_2 = user_security_phase[1]
      user_phase_3 = user_security_phase[2]
      user_phase_4 = user_security_phase[3]
      user_phase_5 = user_security_phase[4]
      user_phase_6 = user_security_phase[5]
      phase1 = validated_data.get("phase1")
      phase2 = validated_data.get("phase2")
      phase3 = validated_data.get("phase3")
      phase4 = validated_data.get("phase4")
      phase5 = validated_data.get("phase5")
      phase6 = validated_data.get("phase6")
      
      if user_phase_1 != phase1:
        raise ValidationError({"message":"value does not match please try again"})
      elif user_phase_2 != phase2:
        raise ValidationError({"message":"value does not match please try again"})
      elif user_phase_3 != phase3:
        raise ValidationError({"message":"value does not match please try again"})
      elif user_phase_4 != phase4:
        raise ValidationError({"message":"value does not match please try again"})
      elif user_phase_5 != phase5:
        raise ValidationError({"message":"value does not match please try again"})
      elif user_phase_6 != phase6:
        raise ValidationError({"message":"value does not match please try again"})
      
      user.security_phase_1 = phase1
      user.security_phase_2 = phase2
      user.security_phase_3 = phase3
      user.security_phase_4 = phase4
      user.security_phase_5 = phase5
      user.security_phase_6 = phase6
      
      user.phase_active = True
      user.save()
      
      refresh = RefreshToken.for_user(user)
      
      refresh['name'] = user.username
      refresh['email'] = user.email
      refresh['active'] = user.phase_active
      refresh['is_superuser'] = user.is_superuser
      
      return Response({
        "message":"Pass key successfully activated",
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        }, status=status.HTTP_200_OK)
    except ValidationError as e:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
      



class UserResetPasswordView(APIView):
  serializer_class = UserResetPasswordSerializer
  
  def post(self, request, *args, **kwargs):
    data = request.data
    serializer = self.serializer_class(data=data)
    if serializer.is_valid(raise_exception=True):
      validated_data = serializer.validated_data
      phase1 = validated_data.get("phase1")
      phase2 = validated_data.get("phase2")
      phase3 = validated_data.get("phase3")
      phase4 = validated_data.get("phase4")
      phase5 = validated_data.get("phase5")
      phase6 = validated_data.get("phase6")
      password = validated_data.get("password")
      validated_data.pop("confirm_password")
      user = get_object_or_404(
        UserModel, 
        security_phase_1 = phase1,
        security_phase_2 = phase2,
        security_phase_3 = phase3,
        security_phase_4 = phase4,
        security_phase_5 = phase5,
        security_phase_6 = phase6,
        )
      
      if user.check_password(password):
        raise ValidationError({"message":"New password cannot be the same as the current password."})
      
      user.set_password(password)
      user.save()
      return Response({"message":"Password Reset"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)