
from django.urls import path,include
from .views import *
urlpatterns = [
   path('', webrtc_test, name='webrtc_test_url'),
   path('signin/', login, name='sign_in'),
   path('signup/', signup, name='sign_up'),
   
   
   
]



