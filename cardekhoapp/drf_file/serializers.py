from rest_framework import serializers
from .. models import Carlist,ShowroomList,Review



# # validators
# def alphanumberic(value):
#     if not str(value).isalnum():
#         raise serializers.ValidationError("Chassis number should be alphanumeric")

# # create the serializer of models to save the complex data in dictionary



# class Carserializers(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField(read_only=True)
#     chassisnumber = serializers.CharField(validators=[alphanumberic])
#     price = serializers.DecimalField(max_digits=9,decimal_places=2)


# def create(self,validated_data):
#     return Carlist.objects.create(**validated_data)



# def update (self,instance,validated_data):
#     instance.name = validated_data.get('name',instance.name)
#     instance.description = validated_data.get('description',instance.description)
#     instance.active = validated_data.get('active',instance.active)
#     instance.chassisnumber = validated_data.get('chassisnumber',instance.chassisnumber)
#     instance.price = validated_data.get('price',instance.price)

#     instance.save()
#     return instance


# # create the Modelserializer of models to save the complex data in dictionary
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields = '__all__'

        
class Carserializers(serializers.ModelSerializer):
    # create the custom Serializers field
    discounted_price = serializers.SerializerMethodField()
    Reviews = ReviewSerializer(many=True,read_only=True)

    class Meta:
        model = Carlist
        #fields = ['id','name','description','active','chassisnumber','price']
        fields = '__all__' # for involving the all model fields 
        #exclude = ['active'] # for excluding the some field from the whole model fields

    def get_discounted_price(self, object):
        discountedprice = object.price - 5000
        return discountedprice

    # validation for particular field
    # field level validations
    def validate_price(self, value):
        if value <= 20000.00:
            raise serializers.ValidationError("Price should be greater than 20000")
        return value

    # validation for object fields

    # object level validations
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and Discription must be different")
        return data
    


class ShowroomSerilaizer(serializers.ModelSerializer):
    showroom = Carserializers(many=True,read_only=True)
    #showroom =  serializers.StringRelatedField(many=True)
    #showroom = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #showroom =  serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='Showroom_details'
    # )
    class Meta:
        model = ShowroomList
        fields = '__all__'

