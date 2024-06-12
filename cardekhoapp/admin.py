from django.contrib import admin
from .models import Carlist,ShowroomList,Review

# Register your models here

admin.site.register(Carlist)

admin.site.register(ShowroomList)

admin.site.register(Review)