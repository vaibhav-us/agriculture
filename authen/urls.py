from django.urls import path
from . import views

urlpatterns = [
    path('sign',views.authen),
    path('signout',views.signout),
    path('getuser/',views.get_user_details)
    
]
