from django.urls import path, include

urlpatterns = [
    path('user/', include('profiles.api.urls')),
    path('packages/', include('packages.api.urls')),
    path('investments/', include('investment.api.urls')),
    path('payments/', include('payments.api.urls')),
    path('admins/', include('admins.api.urls')),
    path('tasks/', include('tasks.api.urls')),
    path('withdrawals/', include('withdrawals.api.urls')),
    # path('api-auth/', include('rest_framework.urls'))
]
