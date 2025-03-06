from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


from rest_framework import serializers
from .models import Usermodel, LoginTable

class LoginTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginTable
        fields = ['id', 'username', 'password', 'email', 'type']

class UserModelSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Usermodel
        fields = '__all__'  # Include all fields

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class UsermodelSerializer1(serializers.ModelSerializer):
    user_pages = LoginTableSerializer()  # Nesting LoginTable data
    skill = SkillSerializer(source='skill_set', many=True, read_only=True)  # Fetch related skills

    class Meta:
        model = Usermodel
        fields = ['id',
            'user_pages', 'fullname', 'Age', 'Date_of_birth', 'Father_name',
            'Mother_name', 'Gender', 'City', 'phonenumber', 'Addar_num',
            'Qualification', 'Address', 'Vehiclenumber', 'Latitude',
            'Longitude', 'University', 'status', 'skill'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Flatten LoginTable data to top level
        user_data = data.pop('user_pages', {})
        return {**user_data, **data}
    
class CategorytableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorytable
        fields = '__all__'

class UsermodelSerializer2(serializers.ModelSerializer):
    user_pages = LoginTableSerializer()  # Nesting LoginTable data
 # Fetch related skills

    class Meta:
        model = Usermodel
        fields = ['id',
            'user_pages', 'fullname', 'Age', 'Date_of_birth', 'Father_name',
            'Mother_name', 'Gender', 'City', 'phonenumber', 'Addar_num',
            'Qualification', 'Address', 'Vehiclenumber', 'Latitude',
            'Longitude', 'University', 'status'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Flatten LoginTable data to top level
        user_data = data.pop('user_pages', {})
        return {**user_data, **data}
from rest_framework import serializers
from .models import Assigntask

class AssigntaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assigntask
        fields = '__all__'


class IncidenttableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidenttable
        fields = '__all__'

class EmergencyalerttableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergencyalerttable
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source='res_cat.category_name', read_only=True)
    cat_id = serializers.CharField(source='res_cat.id', read_only=True)
    class Meta:
        model = Resourcetable
        fields = '__all__'
class AmounttableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amounttable
        fields = '__all__'
class FeedbackSerializer(serializers.ModelSerializer):

    userid_name = serializers.CharField(source='userid.fullname', read_only=True)
    volunteerid_name = serializers.CharField(source='volunteerid.fullname', read_only=True)
    class Meta:
        model = Feedbacktable
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    userid_name = serializers.CharField(source='userid.fullname', read_only=True)
    class Meta:
        model = Requesttable
        fields = '__all__'

class RequesttableSerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(source='resource.res_cat.category_name')
    resource_name=serializers.CharField(source='resource.res_name')
    class Meta:
        model = Requesttable
        fields = '__all__'

class RequesttableSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Requesttable
        fields = '__all__'