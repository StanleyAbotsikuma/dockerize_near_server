

from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('create_account/', UserAuthView.as_view(), name='user-auth'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Staff Endpoints
    path('staff/', StaffViewSet.as_view()),
]
