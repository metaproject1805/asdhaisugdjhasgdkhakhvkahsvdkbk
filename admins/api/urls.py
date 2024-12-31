from django.urls import path
from .views import DailyInvestmentUpdate, DailyUserUpdate, UserCountView, AdminPackageActionView,PendingUserView, InactiveUserView, ActiveUserView, AllUserView, PendingInvestmentUserView,AdminInvestmentActionView, AllWithdrawalView, AdminWithdrawalActionView


urlpatterns = [
    path("user-count/", UserCountView.as_view(), name="user_count_view"),
    path("admin-package-action/<int:pk>/", AdminPackageActionView.as_view(), name="admin_package_view"),
    path("admin-investment-action/<int:pk>/", AdminInvestmentActionView.as_view(), name="admin_investment_view"),
    path("admin-withdrawal-action/<int:pk>/", AdminWithdrawalActionView.as_view(), name="admin_withdrawal_view"),
    path("all-user/", AllUserView.as_view(), name="all_user_view"),
    path("all-withdrawal/", AllWithdrawalView.as_view(), name="all_withdrawal_view"),
    path("active-user/", ActiveUserView.as_view(), name="active_users_view"),
    path("inactive-user/", InactiveUserView.as_view(), name="inactive_users_view"),
    path("pending-user/", PendingUserView.as_view(), name="pending_users_view"),
    path("pending-investment-user/", PendingInvestmentUserView.as_view(), name="pending_investment_users_view"),
    # path("daily-investment-update", DailyInvestmentUpdate.as_view(), name="daily_investment_update"),
    # path("daily-user-update", DailyUserUpdate.as_view(), name="daily_user_update"),
]
