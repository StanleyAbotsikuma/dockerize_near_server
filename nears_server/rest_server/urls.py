

from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserAuthView
urlpatterns = [
    path('user-auth/', UserAuthView.as_view(), name='user-auth'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('test/', protected_view),
   
]
