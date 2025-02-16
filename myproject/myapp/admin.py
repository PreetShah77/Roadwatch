from django.contrib import admin
from .models import Employee, Task, Complaint, CustomUser

admin.site.register(CustomUser)
admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Complaint)
