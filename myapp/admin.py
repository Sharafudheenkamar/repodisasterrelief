from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(LoginTable)
admin.site.register(Usermodel)
admin.site.register(Skill)
admin.site.register(Assigntask)
admin.site.register(Emergencyalerttable)
admin.site.register(Incidenttable)
admin.site.register(Resourcetable)
admin.site.register(Categorytable)
admin.site.register(Feedbacktable)
admin.site.register(Requesttable)
admin.site.register(Amounttable)