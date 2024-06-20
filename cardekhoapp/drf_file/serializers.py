from rest_framework import serializers
from .. models import Carlist,ShowroomList,Review



# # Define a custom validator function to check if a value is alphanumeric
# def alphanumberic(value):
#     # Convert the value to a string
#     str_value = str(value)
    
#     # Check if the string is alphanumeric
#     if not str_value.isalnum():
#         # Raise a validation error if the string is not alphanumeric
#         raise serializers.ValidationError("Chassis number should be alphanumeric")


# // create the serializer of models to save the complex data in dictionary

# # Define a serializer class for Carlist model
# class CarSerializer(serializers.Serializer):
#     # Define a field for the id, which is read-only
#     id = serializers.IntegerField(read_only=True)
    
#     # Define a field for the name, which is a character field
#     name = serializers.CharField()
    
#     # Define a field for the description, which is a character field
#     description = serializers.CharField()
    
#     # Define a field for the active status, which is a boolean field and read-only
#     active = serializers.BooleanField(read_only=True)
    
#     # Define a field for the chassis number, which is a character field with alphanumeric validation
#     chassisnumber = serializers.CharField(validators=[alphanumberic])
    
#     # Define a field for the price, which is a decimal field with 9 digits and 2 decimal places
#     price = serializers.DecimalField(max_digits=9, decimal_places=2)

#     # Define a create method to create a new Carlist instance
#     def create(self, validated_data):
#         # Create a new Carlist instance with the validated data
#         return Carlist.objects.create(**validated_data)

#     # Define an update method to update an existing Carlist instance
#     def update(self, instance, validated_data):
#         # Update the instance's fields with the validated data
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.chassisnumber = validated_data.get('chassisnumber', instance.chassisnumber)
#         instance.price = validated_data.get('price', instance.price)
        
#         # Save the updated instance
#         instance.save()
#         return instance


# # //create the Modelserializer of models to save the complex data in dictionary


# Define a serializer class for Review model
class ReviewSerializer(serializers.ModelSerializer):
    # Define the Meta class to specify the model and fields for the serializer
    class Meta:
        # Specify the model for the serializer
        model = Review
        # Specify that all fields should be included in the serializer
        fields = '__all__'  # Use all fields from the Review model

        
# Define a serializer class for Carlist model
class CarSerializer(serializers.ModelSerializer):
    # Create a custom serializer field to calculate the discounted price
    discounted_price = serializers.SerializerMethodField()
    
    # Define a field for Reviews, which is a many-to-many relationship with Review model
    # Use ReviewSerializer to serialize the related Review objects
    # Set many=True to indicate that this field can have multiple values
    # Set read_only=True to indicate that this field is read-only
    Reviews = ReviewSerializer(many=True, read_only=True)

    # Define the Meta class to specify the model and fields for the serializer
    class Meta:
        # Specify the model for the serializer
        model = Carlist
        # Specify that all fields should be included in the serializer
        fields = '__all__'  # Use all fields from the model
        # Alternatively, you can specify specific fields to include
        # fields = ['id', 'name', 'description', 'active', 'chassisnumber', 'price']
        # Or exclude specific fields
        # exclude = ['active']  # Exclude the 'active' field from the serializer

    # Define a method to calculate the discounted price
    def get_discounted_price(self, object):
        # Calculate the discounted price by subtracting 5000 from the original price
        discountedprice = object.price - 5000
        return discountedprice

    # Define a field-level validation method for the 'price' field
    def validate_price(self, value):
        # Check if the price is less than or equal to 20000
        if value <= 20000.00:
            # Raise a validation error if the price is too low
            raise serializers.ValidationError("Price should be greater than 20000")
        # Return the validated value
        return value

    # Define an object-level validation method
    def validate(self, data):
        # Check if the 'name' and 'description' fields are the same
        if data['name'] == data['description']:
            # Raise a validation error if the fields are the same
            raise serializers.ValidationError("Name and Description must be different")
        # Return the validated data
        return data    


# Define a serializer class for ShowroomList model
class ShowroomSerializer(serializers.ModelSerializer):
    # Define a field for showroom, which is a many-to-many relationship with Car model
    # Use CarSerializer to serialize the related Car objects
    # Set many=True to indicate that this field can have multiple values
    # Set read_only=True to indicate that this field is read-only
    showroom = CarSerializer(many=True, read_only=True)
    
    # The following lines are commented out, but they show alternative ways to serialize the showroom field
    # showroom = serializers.StringRelatedField(many=True)  # Serialize as a string representation of the related objects
    # showroom = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Serialize as the primary key of the related objects
    # showroom = serializers.HyperlinkedRelatedField(  # Serialize as a hyperlink to the related objects
    #     many=True,
    #     read_only=True,
    #     view_name='Showroom_details'  # The view name to use for the hyperlink
    # )
    
    # Define the Meta class to specify the model and fields for the serializer
    class Meta:
        # Specify the model for the serializer
        model = ShowroomList
        # Specify that all fields should be included in the serializer
        fields = '__all__'

