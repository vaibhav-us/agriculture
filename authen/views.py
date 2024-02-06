from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import CustomUser,Crop
from .serializers import CustomUserSerializer,CropSerializer
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt




    
def signup(request):
    user_data = request.data
    user = User.objects.create(username=user_data["user_name"])
    user.save()
    customuser = CustomUser.objects.create(user= user , profile_photo=user_data["profile_pic"])
    customuser.save()
    crops = Crop.objects.create(crop_name=user_data['crop_name'],crop_stage=user_data['crop_stage'],crop_area=user_data['crop_area'])
    crops.save()
    return user


@csrf_exempt
@api_view(['POST'])
def authen(request):

    user_id = request.data["user_id"]
    
    try:
        user = User.objects.get(username = user_id)
    except ObjectDoesNotExist:
        user = None
        return Response("user not found")
    if user:
        login(request,user)
        return Response("authentication success")

@api_view(['GET'])
def signout(request):
    logout(request)
    return Response("logged out")


@api_view(['POST'])
def get_user_details(request):
    username = request.data['user_id']
    user = User.objects.get(username=username)
    custom_user=CustomUser.objects.get(user=user)
    crops = Crop.objects.filter(user=custom_user)
    user_serializer = CustomUserSerializer(custom_user)
    crop_serializer = CropSerializer(crops, many=True)
    return Response({"user":user_serializer.data,"crops":crop_serializer.data})


















