from django.db import models

from django.db import models
from django.template.defaultfilters import default

# Create your models here.

class LoginTable(models.Model):
    username=models.CharField(max_length=100, blank=True,null=True)
    password=models.CharField(max_length=100, blank=True,null=True)
    type=models.CharField(max_length=100, blank=True,null=True,default='college')
    email=models.CharField(max_length=100, blank=True,null=True)



# Create your models here.



class Usermodel(models.Model):
    user_pages = models.ForeignKey(LoginTable, on_delete=models.CASCADE,null=True,blank=True)
    fullname = models.CharField(max_length=25, null=True, blank=True)
    Age = models.IntegerField(null=True, blank=True)
    Date_of_birth = models.DateField(null=True, blank=True)
    Email = models.EmailField(null=True, blank=True)
    Father_name = models.CharField(max_length=20, null=True, blank=True)
    Mother_name = models.CharField(max_length=20, null=True, blank=True)
    Gender = models.CharField(max_length=10, null=True, blank=True)
    City = models.CharField(max_length=20, null=True, blank=True)
    phonenumber = models.IntegerField(null=True, blank=True)
    Addar_num = models.IntegerField(null=True, blank=True)
    Qualification = models.CharField(max_length=20, null=True, blank=True)
    Address = models.CharField(max_length=20, null=True, blank=True)
    Vehiclenumber = models.CharField(max_length=100,null=True,blank=True)
    Latitude = models.CharField(max_length=100,null=True,blank=True)
    Longitude = models.CharField(max_length=100,null=True,blank=True)
    University = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(default="active", max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Skill(models.Model):
    user = models.ForeignKey(Usermodel, on_delete=models.CASCADE,null=True,blank=True)
    skill = models.CharField(max_length=25, null=True, blank=True)

class Assigntask(models.Model):
    userid=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True,blank=True,related_name='assignerid')
    volunteerid=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True,blank=True,related_name='volunteerid')
    task_name = models.CharField(max_length=100, null=True, blank=True)
    task_description = models.CharField(max_length=100, null=True, blank=True)
    task_status = models.CharField(max_length=100, null=True, blank=True)
    task_deadline = models.DateField(null=True, blank=True)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Assigntask, Usermodel
from .serializers import AssigntaskSerializer

class AssignTaskView(APIView):
    def post(self, request):
        """
        Assigns a task to a volunteer.
        Expected Input:
        {
            "userid": 1,   # Assigner's user ID
            "volunteerid": 2,  # Volunteer's user ID
            "task_name": "Distribute Food",
            "task_description": "Deliver food packets to flood victims",
            "task_status": "Pending",
            "task_deadline": "2024-10-01"
        }
        """
        serializer = AssigntaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Task assigned successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, volunteer_id=None):
        """
        Fetches all tasks for a specific volunteer (if `volunteer_id` is provided)
        or all assigned tasks if no ID is given.
        """
        if volunteer_id:
            tasks = Assigntask.objects.filter(volunteerid=volunteer_id)
        else:
            tasks = Assigntask.objects.all()
            
        serializer = AssigntaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
