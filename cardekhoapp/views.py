from django.shortcuts import render
from .models import Carlist,ShowroomList
#from django.http import JsonResponse
from .drf_file.serializers import Carserializers,ShowroomSerilaizer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
# # Create your views here.
# # def car_list_view(request):
# #     cars = Carlist.objects.all()

# #     data = {
# #         "cars": list(cars.values()),
# #     }

# #     return JsonResponse(data)

# # def car_detail(request,pk):
# #     car = Carlist.objects.get(pk=pk)

# #     data = {
# #         "name": car.name,
# #         "description": car.description,
# #         "active": car.active,

# #     }

# #     return JsonResponse(data)

# @api_view()

# def car_list_view(request):
#     cars = Carlist.objects.all()
#     serializer = Carserializers(cars,many=True) 
#     return Response(serializer.data)

# @api_view()
 

# def car_detail(request,pk):
#     cars = Carlist.objects.get(pk=pk)
#     serializer = Carserializers(cars)
#     return Response(serializer.data)


# create new datafield

##Function Based Views

@api_view (['GET','POST'])
def car_list_view(request):
    if request.method == 'GET':
        try:

            cars = Carlist.objects.all()
        except:
            return Response({'error':'car not found'},status= status.HTTP_404_NOT_FOUND)

        serializer = Carserializers(cars,many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = Carserializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        





@api_view(['GET','PUT','DELETE'])
def car_detail(request,pk):
    if request.method == 'GET':
        try:

            cars = Carlist.objects.get(pk=pk)
        except:
            return Response({'error':'car not found'},status= status.HTTP_404_NOT_FOUND)
        
        
        serializer = Carserializers(cars)
        return Response(serializer.data)
    if request.method == 'PUT':
        cars = Carlist.objects.get(pk=pk)
        #print(cars)
        serializer = Carserializers(cars,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        cars = Carlist.objects.get(pk=pk)
        cars.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CLASS BASED VIEWS

class Showroom_View(APIView):

    # apply Authentications and Permissions
    #authentication_classes=[BasicAuthentication]
    #permission_classes=[IsAuthenticated] # it allows thw authenticated user to access
    #permission_classes=[IsAdminUser] # its allow only the admin user to acccess the data
    #for Get Request

    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request):
        showrrom = ShowroomList.objects.all()
        serializer = ShowroomSerilaizer(showrrom,many=True,context={'request': request})
        return Response(serializer.data)
    

    # for Post Request

    def post(self,request):
        serializer =ShowroomSerilaizer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data)

        else:
            return Response(serializer.errors)

class Showroom_details(APIView):
    def get(self,request,pk):
        try:
            showroom = ShowroomList.objects.get(pk=pk)
        except:
            return Response({'error':'showroom not found'},status= status.HTTP_404_NOT_FOUND)
        serializer = ShowroomSerilaizer(showroom)
        return Response(serializer.data)
    def put(self,request,pk):
        showroom = ShowroomList.objects.get(pk=pk)
        serializer = ShowroomSerilaizer(showroom,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        showroom = ShowroomList.objects.get(pk=pk)
        showroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
