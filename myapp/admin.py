from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(LoginTable)
admin.site.register(Usermodel)
admin.site.register(Skill)
admin.site.register(Assigntask)