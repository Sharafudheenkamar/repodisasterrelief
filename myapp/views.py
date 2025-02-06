
from pyexpat.errors import messages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

class LoginPage(APIView):
    def post(self, request):
        response_dict = {}

        # Get data from the request
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate input
        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the user from LoginTable
        t_user = LoginTable.objects.filter(username=username).first()

        if not t_user:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_401_UNAUTHORIZED)



        # Successful login response
        response_dict["message"] = "success"
        response_dict["login_id"] = t_user.id

        return Response(response_dict, status=HTTP_200_OK)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usermodel, LoginTable
from .serializers import LoginTableSerializer, SkillSerializer, UserModelSerializer, UsermodelSerializer1
from django.core.mail import send_mail

from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from .serializers import LoginTableSerializer, UserModelSerializer
from .models import LoginTable, Usermodel

class UserRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # First, Serialize login data (LoginTable)
        skills_data = request.data.pop('skill', [])
        data={}
        data=request.data
        if skills_data:
            data['type']='volunteer'
        elif request.data['Vehiclenumber']:
            data['type']='ambulance'
        else :
            data['type']='user'
        
        serializer1 = LoginTableSerializer(data=data)

        # Then, Serialize user data (Usermodel)
        serializer = UserModelSerializer(data=request.data)

        # Validate both serializers
        if serializer.is_valid() and serializer1.is_valid():
            # Save the login data first and associate the created instance
            login_data = serializer1.save()

            # Now, save the user data, associating it with the LoginTable (login_data)
            # Use the 'user_pages' foreign key to link the Usermodel with LoginTable
            user_data = serializer.save(user_pages=login_data)
            for skill in skills_data:
                skill['user'] = user_data.id  # Associate user ID with skills
                skill_serializer = SkillSerializer(data=skill)
                if skill_serializer.is_valid():
                    skill_serializer.save(user=user_data)

            # Send a confirmation email to the user
            if skills_data:
                subject = "Registration Successful"
                message = f"Hello {request.data['fullname']},\n\nYou have successfully registered."
                from_email = "no-reply@yourdomain.com"
                recipient_list = [request.data['email']]
            
                send_mail(subject, message, from_email, recipient_list)
            


            # Respond with a success message
            return Response({
                "message": "User registered successfully. A confirmation email has been sent.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        # Return error response if validation fails
        return Response({
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
# {
#     "username": "john_doe",
#     "password": "securepassword123",
#     "email": "john@example.com",
#     "fullname": "John Doe",
#     "Age": 25,
#     "Date_of_birth": "1998-05-10",
#     "Father_name": "Robert Doe",
#     "Mother_name": "Jane Doe",
#     "Gender": "Male",
#     "City": "New York",
#     "phonenumber": 9876543210,
#     "Addar_num": 123456789012,
#     "Qualification": "Bachelor",
#     "Address": "123 Main St",
#     "Vehiclenumber": "NY-1234",
#     "Latitude": "40.7128",
#     "Longitude": "-74.0060",
#     "University": "NYU",
#     "status": "active",
#     "skill": [
#         {"skill": "Python"},
#         {"skill": "Django"}
#     ]
# }
class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = Usermodel.objects.get(id=user_id)
            serializer = UsermodelSerializer1(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usermodel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LoginTable, Usermodel, Skill
from .serializers import UserModelSerializer, LoginTableSerializer, SkillSerializer

class AmbulanceUserListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Filter users where user_pages (LoginTable) has type='ambulance'
            ambulance_users = Usermodel.objects.filter(user_pages__type='ambulance')
            
            users_list = []
            for user in ambulance_users:
                login_data = LoginTableSerializer(user.user_pages).data
                user_data = UsermodelSerializer1(user).data
                
                # Fetch skills associated with the user
                skills = Skill.objects.filter(user=user)
                skill_data = SkillSerializer(skills, many=True).data
                
                # Combine login, user, and skill data into one response format
                combined_data = {**login_data, **user_data, "skill": skill_data}
                users_list.append(combined_data)

            return Response(users_list, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VolunteerUserListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Filter users where user_pages (LoginTable) has type='ambulance'
            ambulance_users = Usermodel.objects.filter(user_pages__type='ambulance')
            
            users_list = []
            for user in ambulance_users:
                login_data = LoginTableSerializer(user.user_pages).data
                user_data = UsermodelSerializer1(user).data
                
                # Fetch skills associated with the user
                skills = Skill.objects.filter(user=user)
                skill_data = SkillSerializer(skills, many=True).data
                
                # Combine login, user, and skill data into one response format
                combined_data = {**login_data, **user_data, "skill": skill_data}
                users_list.append(combined_data)

            return Response(users_list, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
