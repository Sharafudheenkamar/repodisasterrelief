
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
        # Extract and process request data
        data={}
        data = request.data 
        print(request.data) # Ensure data is mutable
        skills_data = data.pop('skills', [])  # Extract skills safely

        # Assign 'username' from 'Email'
        data['username'] = data.get('Email', '')

        # # Determine user type
        # if skills_data:
        #     data['type'] = 'volunteer'
        # elif data.get('Vehiclenumber'):
        #     data['type'] = 'ambulance'
        # else:
        #     data['type'] = 'user'

        # Extract and handle the image if provided
        image = data.get('Image', None)

        # Serialize login data (LoginTable)
        serializer1 = LoginTableSerializer(data=data)

        # Serialize user data (Usermodel)
        serializer = UserModelSerializer(data=data)

        # Validate both serializers
        if serializer1.is_valid() and serializer.is_valid():
            # Save login data first
            login_data = serializer1.save()

            # Save user data, linking it to login_data
            user_data = serializer.save(user_pages=login_data)

            # Save skills if provided
            for skill_name in skills_data:
                skill_serializer = SkillSerializer(data={'skill': skill_name, 'user': user_data.id})
                if skill_serializer.is_valid():
                    skill_serializer.save()

            # Send confirmation email if skills exist
            # if skills_data:
            #     subject = "Registration Successful"
            #     message = f"Hello {data.get('fullname', 'User')},\n\nYou have successfully registered as a {data['type']}."
            #     from_email = "no-reply@yourdomain.com"
            #     recipient_list = [data.get('Email', '')]

            #     send_mail(subject, message, from_email, recipient_list)

            # Return success response
            return Response({
                "message": "User registered successfully. A confirmation email has been sent.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        # Return validation errors if any
        return Response({
            "message": "Validation failed",
            "errors": {**serializer.errors, **serializer1.errors}
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
            ambulance_users = Usermodel.objects.filter(user_pages__type='volunteer').all()
            # print(ambulance_users)
            
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
                # print(users_list)

            return Response(users_list, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Assigntask, Usermodel
from .serializers import AssigntaskSerializer

class AssignTaskView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print("ddddddddddddd",request.data)
        userid = data.get('userid')
        task_name = data.get('task_name')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        volunteers = data.get('volunteers', [])
        
        # Get user who is assigning the task
        try:
            user = Usermodel.objects.get(user_pages__id=userid)
        except Usermodel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        assigned_tasks = []
        for volunteer_data in volunteers:
            volunteer_id = volunteer_data.get('id')
            print("ddddddddddddddddddddn,mnv,mxnvmn",volunteer_id)
            try:
                volunteer = Usermodel.objects.get(id=volunteer_id)
            except Usermodel.DoesNotExist:
                return Response({'error': f'Volunteer with ID {volunteer_id} not found'}, status=status.HTTP_404_NOT_FOUND)
            print("22222222222222222")
            # Create task assignment
            task = Assigntask.objects.create(
                userid=user,
                volunteerid=volunteer,
                task_name=task_name,
                latitude=latitude,
                longitude=longitude,
                task_status='Pending'  # Default status
            )
            assigned_tasks.append(task)
        print("dddddddfdsn,mxcvn,mnxcz,mxn,zmnoiaw9euqur09u")
        serializer = AssigntaskSerializer(assigned_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
class LoginPageApi(APIView):
    def post(self, request):
        response_dict= {}
        password = request.data.get("password")
        print("Password ------------------> ",password)
        username = request.data.get("username")
        print("Username ------------------> ",username)
        try:
            userobj = LoginTable.objects.filter(username=username, password=password).first()
            print(userobj)
            response_dict = {
                "login_id": userobj.id,
                "user_type": userobj.type,
                "status": "success",
            }   
            print("User details :--------------> ",response_dict)
            return Response(response_dict, HTTP_200_OK)
            # print("user_obj :-----------", user)
        except LoginTable.DoesNotExist:
            response_dict["message"] = "No account found for this username. Please signup."
            return Response(response_dict, HTTP_200_OK)
      
        

        
