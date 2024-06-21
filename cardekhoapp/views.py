from django.shortcuts import render
from .models import *
#from django.http import JsonResponse
from .drf_file.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser,DjangoModelPermissions
from rest_framework import mixins
from rest_framework import generics

# #// Create your views here.


# Define a view function to retrieve a list of all cars
# def car_list_view(request):
#     # Retrieve all car objects from the database
#     cars = Carlist.objects.all()
    
#     # Convert the car objects to a list of dictionaries
#     # Each dictionary represents a car, with keys for name, description, and active status
#     data = {
#         "cars": list(cars.values()),
#     }
    
#     # Return the list of cars as a JSON response
#     return JsonResponse(data)

# # Define a view function to retrieve a single car by its primary key (pk)
# def car_detail(request, pk):
#     # Retrieve the car object with the specified primary key (pk)
#     car = Carlist.objects.get(pk=pk)
    
#     # Create a dictionary to store the car's details
#     data = {
#         # Include the car's name
#         "name": car.name,
#         # Include the car's description
#         "description": car.description,
#         # Include the car's active status
#         "active": car.active,
#     }
    
#     # Return the car's details as a JSON response
#     return JsonResponse(data)

# Define a view function to handle GET requests for car lists
# @api_view(['GET'])  # Decorator to specify the allowed HTTP method
# def car_list_view(request):
#     # Retrieve all car lists from the database
#     cars = Carlist.objects.all()
#     # Serialize the car lists using the Carserializers
#     serializer = Carserializers(cars, many=True)  
#     # Return the serialized data in the response
#     return Response(serializer.data)

# # Define a view function to handle GET requests for a single car detail
# @api_view(['GET'])  # Decorator to specify the allowed HTTP method
# def car_detail(request, pk):
#     # Retrieve a single car list from the database by its primary key (pk)
#     cars = Carlist.objects.get(pk=pk)
#     # Serialize the car list using the Carserializers
#     serializer = Carserializers(cars)
#     # Return the serialized data in the response
#     return Response(serializer.data)

# create new datafield

## //Function Based Views

# Define a view function to handle GET and POST requests for car lists
@api_view(['GET', 'POST'])
def car_list_view(request):
    # Handle GET requests
    if request.method == 'GET':
        try:
            # Retrieve all car lists from the database
            cars = Carlist.objects.all()
        except:
            # Return a 404 error response if no cars are found
            return Response({'error': 'car not found'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the car lists using the Carserializers
        serializer = CarSerializer(cars, many=True)
        # Return the serialized data in the response
        return Response(serializer.data)

    # Handle POST requests
    if request.method == 'POST':
        # Create a new serializer instance with the request data
        serializer = CarSerializer(data=request.data)
        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the serializer data to the database
            serializer.save()
            # Return the saved data in the response
            return Response(serializer.data)
        else:
            # Return a 400 error response with the serializer errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



### car_detail function
@api_view(['GET', 'PUT', 'DELETE'])
def car_detail(request, pk):
    """
    A function-based view that handles GET, PUT, and DELETE requests for a single car.
    
    The function takes a request object and a primary key (pk) as arguments.
    """
    
    # Handle GET requests
    if request.method == 'GET':
        """
        Retrieve a single car by its primary key.
        
        If the car is not found, return a 404 error response.
        """
        try:
            cars = Carlist.objects.get(pk=pk)
        except:
            return Response({'error': 'car not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the car object
        serializer = CarSerializer(cars)
        return Response(serializer.data)
    
    # Handle PUT requests
    if request.method == 'PUT':
        """
        Update a single car by its primary key.
        
        Deserialize the request data, validate it, and save it to the database if valid.
        If the data is invalid, return a 400 error response.
        """
        cars = Carlist.objects.get(pk=pk)
        #print(cars)  # Debugging statement
        serializer = CarSerializer(cars, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle DELETE requests
    if request.method == 'DELETE':
        """
        Delete a single car by its primary key.
        
        Retrieve the car object and delete it from the database.
        Return a 204 response to indicate success.
        """
        cars = Carlist.objects.get(pk=pk)
        cars.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# // CLASS BASED VIEWS

### Showroom_View class
class Showroom_View(APIView):
    """
    A class-based view that handles GET and POST requests for showrooms.
    """
    #authentication_classes=[BasicAuthentication]
    #permission_classes=[IsAuthenticated] # it allows thw authenticated user to access
    #permission_classes=[IsAdminUser] # its allow only the admin user to acccess the data
    # Apply authentication and permission classes
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    """
    This view requires authentication using session authentication, and only allows 
    authenticated users to access the data.
    """
    
    def get(self, request):
        """
        Handle GET requests to retrieve a list of showrooms.
        
        Retrieves all showroom objects from the database, serializes them, and returns 
        the serialized data in the response.
        """
        showrooms = ShowroomList.objects.all()
        serializer = ShowroomSerializer(showrooms, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        """
        Handle POST requests to create a new showroom.
        
        Deserializes the request data, validates it, and saves it to the database if 
        valid. Returns the serialized data in the response.
        """
        serializer = ShowroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)






### Showroom_details class

class Showroom_details(APIView):
    """
    A class-based view that handles GET, PUT, and DELETE requests for a single showroom.
    """
    
    def get(self, request, pk):
        """
        Handle GET requests to retrieve a single showroom.
        
        Retrieves the showroom object with the specified primary key from the database, 
        serializes it, and returns the serialized data in the response. If the showroom 
        is not found, returns a 404 error response.
        """
        try:
            showroom = ShowroomList.objects.get(pk=pk)
        except:
            return Response({'error': 'showroom not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ShowroomSerializer(showroom)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        Handle PUT requests to update a single showroom.
        
        Retrieves the showroom object with the specified primary key from the database, 
        deserializes the request data, validates it, and saves it to the database if 
        valid. Returns the serialized data in the response. If the data is invalid, 
        returns a 400 error response.
        """
        showroom = ShowroomList.objects.get(pk=pk)
        serializer = ShowroomSerializer(showroom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a single showroom.
        
        Retrieves the showroom object with the specified primary key from the database 
        and deletes it. Returns a 204 response to indicate success.
        """
        showroom = ShowroomList.objects.get(pk=pk)
        showroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# // VIEWSSETS AND ROUTERS


# Define a ViewSet class named Showroom_Viewset that inherits from viewsets.Viewset
class Showroom_Viewset(viewsets.ViewSet):
    """
    This ViewSet handles CRUD operations for Showroom models.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [DjangoModelPermissions]
    # Define a method to handle GET requests to retrieve a list of all showrooms
    def list(self, request):
        """
        Returns a list of all showrooms.
        """
        # Retrieve all showroom objects from the database
        queryset = ShowroomList.objects.all()
        
        # Serialize the queryset into a JSON response
        serializers = ShowroomSerializer(queryset, many=True)
        
        # Return the serialized data as a response
        return Response(serializers.data)
    
    # Define a method to handle GET requests to retrieve a single showroom by ID
    def retrieve(self, request, pk=None):
        """
        Returns a single showroom by ID.
        """
        # Retrieve all showroom objects from the database
        queryset = ShowroomList.objects.all()
        
        # Get the showroom object with the specified ID, or raise a 404 error if not found
        showroom = get_object_or_404(queryset, pk=pk)
        
        # Serialize the showroom object into a JSON response
        serializers = ShowroomSerializer(showroom)
        
        # Return the serialized data as a response
        return Response(serializers.data)
    
    # Define a method to handle POST requests to create a new showroom
    def create(self, request):
        """
        Creates a new showroom.
        """
        # Create a serializer instance with the request data
        serializers = ShowroomSerializer(data=request.data)
        
        # Check if the serializer is valid
        if serializers.is_valid():
            # Save the serializer data to the database
            serializers.save()
            
            # Return the serialized data as a response
            return Response(serializers.data)
        else:
            # Return an error response with the serializer errors
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a single showroom.
        
        Retrieves the showroom object with the specified primary key from the database 
        and deletes it. Returns a 204 response to indicate success.
        """
        showroom = ShowroomList.objects.get(pk=pk)
        showroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# // CREATE THE VIEWS USING THE GENIERICVIEWS AND MIXINS

# class ReviewList(mixins.ListModelMixin, 
#                  mixins.CreateModelMixin, 
#                  generics.GenericAPIView):
#     """
#     A class-based view that handles both listing and creating reviews.
    
#     It inherits from GenericAPIView, ListModelMixin, and CreateModelMixin to provide 
#     built-in functionality for listing and creating reviews.
#     """
    
#     # Define the queryset that this view will operate on
#     queryset = Review.objects.all()
#     """
#     This queryset retrieves all review objects from the database.
#     """
    
#     # Define the serializer class that will be used for serialization and deserialization
#     serializer_class = ReviewSerializer
#     """
#     This serializer class is responsible for converting Review objects to JSON data 
#     and vice versa.
#     """


#     authentication_classes = [SessionAuthentication]
#     permission_classes = [DjangoModelPermissions]
    
#     """Add the Django model permission"""
#     def get(self, request, *args, **kwargs):
#         """
#         Handle GET requests to list all reviews.
        
#         Calls the list method provided by ListModelMixin to return a list of reviews.
#         """
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         """
#         Handle POST requests to create a new review.
        
#         Calls the create method provided by CreateModelMixin to create a new review.
#         """
#         return self.create(request, *args, **kwargs)
    



# class ReviewDetails(mixins.RetrieveModelMixin, 
#                     generics.GenericAPIView):
#     """
#     A class-based view that handles retrieving a single review.
    
#     It inherits from GenericAPIView and RetrieveModelMixin to provide 
#     built-in functionality for retrieving a review.
#     """
    
#     # Define the queryset that this view will operate on
#     queryset = Review.objects.all()
#     """
#     This queryset retrieves all review objects from the database.
#     """
    
#     # Define the serializer class that will be used for serialization and deserialization
#     serializer_class = ReviewSerializer
#     """
#     This serializer class is responsible for converting Review objects to JSON data 
#     and vice versa.
#     """
    
#     def get(self, request, *args, **kwargs):
#         """
#         Handle GET requests to retrieve a single review.
        
#         Calls the retrieve method provided by RetrieveModelMixin to return a single review.
#         The retrieve method will automatically handle the lookup of the review by its ID.
#         """
#         return self.retrieve(request, *args, **kwargs)
    

# //CREATE THE VIEWS USING THE CONCRETE VIEWS CLASSES USING ONLY GENERICS NOT MIXINS


# Define a class-based view for listing and creating reviews
class ReviewList(generics.ListCreateAPIView):
    """
    This view handles GET and POST requests for reviews.
    GET requests will return a list of all reviews.
    POST requests will create a new review.
    """
    # Define the queryset that will be used to retrieve reviews
    queryset = Review.objects.all()
    
    # Specify the serializer class that will be used to serialize and deserialize reviews
    serializer_class = ReviewSerializer

    authentication_classes = [SessionAuthentication]
    permission_classes = [DjangoModelPermissions]


# Define a class-based view for retrieving, updating, and deleting individual reviews
class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    This view handles GET, PUT, and DELETE requests for individual reviews.
    GET requests will return a single review.
    PUT requests will update a single review.
    DELETE requests will delete a single review.
    """
    # Define the queryset that will be used to retrieve reviews
    # This will allow the view to retrieve a single review by its ID
    queryset = Review.objects.all()
    
    # Specify the serializer class that will be used to serialize and deserialize reviews
    # This serializer will be used to validate and convert data for the review
    serializer_class = ReviewSerializer    

    authentication_classes = [SessionAuthentication]
    permission_classes = [DjangoModelPermissions]
    
    # apply the basic authentications to the page

