from django.contrib import admin
from .models import CustomUser
from .models import Crop

admin.site.register(CustomUser)
admin.site.register(Crop)
