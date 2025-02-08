from django.db import models
# Create your models here.

class LoginTable(models.Model):
    username=models.CharField(max_length=100, blank=True,null=True)
    password=models.CharField(max_length=100, blank=True,null=True)
    type=models.CharField(max_length=100, blank=True,null=True)
    email=models.CharField(max_length=100, blank=True,null=True)



# Create your models here



class Usermodel(models.Model):
    user_pages = models.ForeignKey(LoginTable, on_delete=models.CASCADE,null=True,blank=True)
    fullname = models.CharField(max_length=25, null=True, blank=True)
    Age = models.IntegerField(null=True, blank=True)
    Date_of_birth = models.DateField(null=True, blank=True)
    Image = models.FileField(upload_to='profileimages',null=True,blank=True)
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
    latitude = models.CharField(max_length=100,null=True,blank=True)
    longitude = models.CharField(max_length=100,null=True,blank=True)
    task_status = models.CharField(max_length=100, null=True, blank=True)
    task_deadline = models.DateField(null=True, blank=True)

