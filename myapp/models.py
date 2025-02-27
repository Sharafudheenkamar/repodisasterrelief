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


class Incidenttable(models.Model):
    userid=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True,blank=True,related_name='assigner_id')
    volunteerid=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True,blank=True,related_name='volunteer_id')
    incident_name = models.CharField(max_length=100, null=True, blank=True)
    incident_description = models.CharField(max_length=100, null=True, blank=True)
    incident_latitude = models.CharField(max_length=100,null=True,blank=True)
    incident_longitude = models.CharField(max_length=100,null=True,blank=True)
    reported_date= models.DateField(null=True, blank=True)


class Emergencyalerttable(models.Model):
    userid=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True,blank=True,related_name='alert_assigner_id')
    volunteerid=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True,blank=True,related_name='alert_volunteer_id')
    alert_name = models.CharField(max_length=100, null=True, blank=True)
    alert_description = models.CharField(max_length=100, null=True, blank=True)
    alert_latitude = models.CharField(max_length=100,null=True,blank=True)
    alert_longitude = models.CharField(max_length=100,null=True,blank=True)
    alert_reported_date= models.DateField(null=True, blank=True)

class Categorytable(models.Model):
    category_name = models.CharField(max_length=100, null=True, blank=True)
    category_description = models.CharField(max_length=100, null=True, blank=True)
    category_status = models.CharField(max_length=100, null=True, blank=True)



class Resourcetable(models.Model):
    userid=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True,blank=True,related_name='resource_assigner_id')
    volunteerid=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True,blank=True,related_name='resource_volunteer_id')
    res_name = models.CharField(max_length=100, null=True, blank=True)
    res_description = models.CharField(max_length=100, null=True, blank=True)
    res_cat = models.ForeignKey(Categorytable,on_delete=models.CASCADE,null=True,blank=True)
    res_amount = models.CharField(max_length=100,null=True,blank=True)
    res_quantity = models.CharField(max_length=100,null=True,blank=True)
    inc_id= models.ForeignKey(Incidenttable,on_delete=models.CASCADE,null=True,blank=True)
class Requesttable(models.Model):
    userid=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True,blank=True,related_name='request_id')
    resource=models.ForeignKey(Resourcetable,on_delete=models.CASCADE,null=True,blank=True)
    request_name = models.CharField(max_length=100, null=True, blank=True)
    request_description = models.CharField(max_length=100, null=True, blank=True)
    request_quantity = models.CharField(max_length=100, null=True, blank=True)
    request_allocated_quantity=models.CharField(max_length=100, null=True, blank=True)
    request_status=models.CharField(max_length=100,null=True,blank=True,default='pending')
    def save(self, *args, **kwargs):
        if self.resource and self.request_allocated_quantity:
            try:
                allocated_quantity = int(self.request_allocated_quantity)
                if allocated_quantity > 0 and self.resource.res_quantity:
                    current_quantity = int(self.resource.res_quantity)
                    
                    if allocated_quantity <= current_quantity:
                        self.resource.res_quantity = str(current_quantity - allocated_quantity)
                        self.resource.save()
                    else:
                        raise ValueError("Allocated quantity cannot be greater than available resource quantity.")
            except ValueError:
                raise ValueError("Invalid quantity format. Ensure it's a valid number.")

        super(Requesttable, self).save(*args, **kwargs)
    

class Feedbacktable(models.Model):
    userid=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True,blank=True,related_name='feedback_assigner_id')
    volunteerid=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True,blank=True,related_name='feedback_volunteer_id')
    feedback_name = models.CharField(max_length=100, null=True, blank=True)
    feedback_description = models.CharField(max_length=100, null=True, blank=True)
    feedback_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    inc_id= models.ForeignKey(Incidenttable,on_delete=models.CASCADE,null=True,blank=True)



