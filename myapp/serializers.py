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
