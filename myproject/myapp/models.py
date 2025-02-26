from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import random
import string
from django.utils.timezone import now

# Custom user manager to handle creation of admin and general users
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Creates a superuser with special permissions
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=60, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Django's hashed password field
    joining_date = models.DateField(default=timezone.now)
    joining_time = models.TimeField(default=timezone.now)
    phone = models.CharField(max_length=10, null=True, blank=True)
    
    # Admin and government role-specific attributes
    is_admin = models.BooleanField(default=False)
    is_government_official = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        # Automatically set full_name and is_government_official based on is_admin when saving
        self.full_name = f"{self.first_name} {self.last_name}"
        if self.is_admin==1 :
            self.is_government_official = self.is_admin  # Set is_government_official to match is_admin
        super().save(*args, **kwargs)

    # Permission methods for admin and government roles
    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_government_official

    def has_module_perms(self, app_label):
        return self.is_admin or self.is_government_official

    def __str__(self):
        return self.full_name


# Complaint model to store reported issues and allow status updates

class Complaint(models.Model):
    complaint_id = models.CharField(max_length=8, unique=True, blank=True)
    issue_type_choices = [
        ('pothole', 'Pothole'),
        ('crack', 'Crack'),
    ]
    issue_type = models.CharField(max_length=50, choices=issue_type_choices)
    severity_choices = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    severity = models.CharField(max_length=10, choices=severity_choices)
    description = models.TextField()
    location = models.CharField(max_length=255, default='Mehsana')
    coordinates = models.CharField(max_length=100)  # For storing latitude, longitude
    image = models.ImageField(upload_to='reports/images/')  # Path for uploaded images
    google_drive_url = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()

    issue_status_choices = [
        ('pending', 'Pending'),
        ('in-progress', 'In-Progress'),
        ('resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=50, choices=issue_status_choices, default='pending')
    resolved_on = models.TextField()  # New field for resolution date
    comment = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Check if status has changed to "resolved"
        if self.status == 'resolved' and self.resolved_on == "":
            self.resolved_on = timezone.now()  # Set resolved_on to current date and time
        elif self.status != 'resolved':
            self.resolved_on = " "  # Reset resolved_on if status changes back

        # Generate random complaint ID if not set
        if not self.complaint_id:
            self.complaint_id = self.generate_complaint_id()
        super().save(*args, **kwargs)

    def generate_complaint_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def __str__(self):
        return f"Report #{self.complaint_id} - {self.issue_type} - {self.severity}"



class Employee(AbstractBaseUser):
    
    emp_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, default="employee@123")
    phone = models.CharField(max_length=15, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    role_choices = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
    ]
    role = models.CharField(max_length=20, choices=role_choices)

    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new instance, set the hashed password and emp_id
            self.password = make_password(self.password)
            
            # Generate emp_id starting from 1001
            last_emp = Employee.objects.all().order_by('emp_id').last()
            if last_emp:
                last_emp_id = int(last_emp.emp_id)
                self.emp_id = str(last_emp_id + 1)
            else:
                self.emp_id = '1001'  # Start from 1001 if no previous employees

            try :
                #Create CustomUser record when Employee record is created and is admin
                if self.role == 'admin':
                    custom_user = CustomUser(
                        first_name=self.first_name,
                        last_name=self.last_name,
                        email=self.email,
                        password=self.password,  # Use hashed password
                        phone=self.phone,
                        is_admin=True,  # Mark as government official
                        last_login=now()
                    )
                else:
                #Create CustomUser record when Employee is created and not admin
                    custom_user = CustomUser(
                        first_name=self.first_name,
                        last_name=self.last_name,
                        email=self.email,
                        password=self.password,  # Use hashed password
                        phone=self.phone,
                        is_government_official=True,  # Mark as government official
                        last_login=now()
                    )
                custom_user.save()  # Save the CustomUser record
            except Exception as e:
                print(f"Error creating CustomUser as email already exists: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"
    

class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('logging_complaint', 'Logging Complaint'),
        ('change_status', 'Change Complaint Status'),
        ('generate_report', 'Generate Report'),
        ('assign_task', 'Assign Task'),  # If you want to assign tasks to others
    ]
    
    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)
    description = models.TextField()
    assigned_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="assigned_tasks")
    complaint = models.ForeignKey('Complaint', on_delete=models.SET_NULL, null=True, blank=True)  # Link to complaint if the task is complaint-related
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Task {self.get_task_type_display()} assigned to {self.assigned_employee.first_name} {self.assigned_employee.last_name}"


# Additional models for settings and user management
class SystemSettings(models.Model):
    setting_name = models.CharField(max_length=50)
    setting_value = models.TextField()

    def __str__(self):
        return f"{self.setting_name}: {self.setting_value}"

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Your existing CustomUser and other models here...

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    # Add any additional fields you want to track
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile of {self.user.full_name}"
    
# Signal to create/update UserProfile when CustomUser is created/updated
@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Update the profile if it exists
        UserProfile.objects.get_or_create(user=instance)