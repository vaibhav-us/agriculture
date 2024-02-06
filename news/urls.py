from django.urls import path
from . import views

urlpatterns = [
    path('home/<str:usr>',views.home)
]
