from .views import SuperUserRegistrationView, UserRegistrationView, UserDetailView, PassKeyPhaseActivateView, UserResetPasswordView, ReadUserNotification
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name="user-registration"),
    # path('register/active-super-user/', SuperUserRegistrationView.as_view(), name="super_user-registration"),
    path('reset-password/', UserResetPasswordView.as_view(), name="user-reset-password"),
    path('detail/<int:pk>/', UserDetailView.as_view(), name="user-detail-view"),
    path('read-notification/<int:pk>/', ReadUserNotification.as_view(), name="read-notification-view"),
    path('pass-key-activate/', PassKeyPhaseActivateView.as_view(), name="user-pass-activate-view"),
    
]
