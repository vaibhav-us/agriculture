from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import CustomUser,Crop, CropSensorData, CropSchedule
from .serializers import CustomUserSerializer,CropSerializer,CropSensorDataSerializer,CropScheduleSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from .utility import capitalizeDict




    
def signup(request):
    user_data = request.data
    user = User.objects.create(username=user_data["user_name"])
    user.save()
    customuser = CustomUser.objects.create(user= user , profilePhoto=user_data["profile_pic"])
    customuser.save()
    crops = Crop.objects.create(name=user_data['crop_name'],stage=user_data['crop_stage'],area=user_data['crop_area'])
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

##new views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getuser_crops(request):
    custom_user = CustomUser.objects.get(user=request.user)

    crops = Crop.objects.filter(user=custom_user)
    cropSerializer = CropSerializer(crops, many=True)
    cropData = []
    for crop in cropSerializer.data:
        cropInstance = Crop.objects.get(id=crop['id'])  # Get Crop instance by ID
        sensorDataInstance = CropSensorData.objects.get(crop=cropInstance)
        condition = CropSensorDataSerializer(sensorDataInstance, many=False).data['condition']
        crop['condition'] = condition
        
        cropData.append(capitalizeDict(crop))
    
    return Response(cropData)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getcrop_schedule(request) :
    custom_user = CustomUser.objects.get(user=request.user)
    crop = request.GET.get('crop')

    #getting instances
    cropInstance = Crop.objects.get(user=custom_user,name=crop )
    sensorDataInstance = CropSensorData.objects.get(crop=cropInstance)
    scheduleInstances = CropSchedule.objects.filter(crop = cropInstance)
    
    #getting data from instances
    crop = CropSerializer(cropInstance, many=False).data
    sensorData = CropSensorDataSerializer(sensorDataInstance, many=False).data
    schedule = CropScheduleSerializer(scheduleInstances, many=True).data 

    #merging separte columns of nitrogen ,phosphorous and potassium together
    sensorData['npk'] = [                  
        sensorData.pop('nitrogen'),
        sensorData.pop('phosphorous'),
        sensorData.pop('potassium'),
    ]
    sensorData['id'] = sensorData.pop('crop') #replacing the primary key of sensor data with its foreign key crop.As they are onetoone relation, it shouldnt be a problem    
    
    #putting everything together
    crop.update(sensorData)
    crop = capitalizeDict(crop)
    crop['schedule'] = capitalizeDict(schedule)

    return Response(crop)

















