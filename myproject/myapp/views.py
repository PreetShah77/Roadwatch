# views.py
import json
import re
import os
import random
import string
from datetime import datetime, date
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.utils.html import format_html   
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Complaint, Employee, Task
from django.core.files.storage import FileSystemStorage
from .forms import EmployeeForm, TaskForm
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from ultralytics import YOLO
from io import BytesIO  # Add this at the top with other imports
from django.core.files.base import ContentFile  # Add this import too
from PIL import Image
import numpy as np
from django.conf import settings
from math import radians, sin, cos, sqrt, atan2
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint
from django.http import HttpRequest



# def raise_complaint(request):
#     if request.method == 'POST':
#         # Get form data
#         issue_type = request.POST['issue_type']
#         severity = request.POST['severity']
#         description = request.POST['description']
#         coordinates = request.POST['coordinates']
#         location = request.POST['location']
        
#         # Create and save the report first without image
#         report = Complaint(
#             issue_type=issue_type,
#             severity=severity,
#             description=description,
#             coordinates=coordinates,
#             location=location,
#         )
#         report.save()  # Save first to generate the complaint ID
        
#         # Handle image upload, detection, and storage
#         if 'image' in request.FILES:
#             image = request.FILES['image']
#             fs = FileSystemStorage()
            
#             image_extension = os.path.splitext(image.name)[1]
            
#             # Save the uploaded image temporarily
#             temp_image_name = f"temp_{report.complaint_id}{image_extension}"
#             temp_image_path = fs.save(temp_image_name, image)
            
#             try:
#                 # Run object detection on the image
#                 detected_info = detector.detect(fs.path(temp_image_path))
                
#                 # Add detection results to the report
#                 report.detected_objects = detected_info['objects']
#                 report.confidence_scores = detected_info['confidence_scores']
#                 report.bounding_boxes = detected_info['bounding_boxes']
                
#                 # Rename and save the final image
#                 final_image_name = f"{report.complaint_id}{image_extension}"
#                 os.rename(fs.path(temp_image_path), fs.path(final_image_name))
                
#                 # Update the report with the image URL and detection results
#                 report.image = final_image_name
#                 report.save()
                
#                 messages.success(request, "Complaint raised successfully with object detection!")
            
#             except Exception as e:
#                 # Handle any errors during detection
#                 messages.error(request, f"Error during object detection: {str(e)}")
#                 # Clean up temporary file
#                 fs.delete(temp_image_path)
                
#                 # Still save the complaint, but without detection results
#                 final_image_name = f"{report.complaint_id}{image_extension}"
#                 image_url = fs.save(final_image_name, image)
#                 report.image = image_url
#                 report.save()
        
#         return redirect(raise_complaint)
    
#     return render(request, 'raise.html')
@login_required
def raise_complaint(request):
    user = request.user
    if not user:
        return redirect('login')

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def normalize_coordinates(coord_str):
        try:
            lat, lon = map(float, coord_str.split(','))
            lat = round(lat, 6)  # Round to 6 decimal places (~1 meter precision)
            lon = round(lon, 6)
            return f"{lat},{lon}"
        except ValueError:
            return None

    if request.method == 'POST':
        severity = request.POST.get('severity', '')
        description = request.POST.get('description', '')
        coordinates = request.POST.get('coordinates', None)
        location = request.POST.get('location', '')

        print(f"User: {user.email}")
        print(f"POST data - Severity: {severity}, Coordinates: {coordinates}, Location: {location}")

        if not (severity and coordinates and location):
            if not coordinates:
                messages.error(request, "Please select a location on the map.")
            else:
                messages.error(request, "All fields are required.")
            return redirect('raise_complaint')

        email = user.email
        coordinates = normalize_coordinates(coordinates)
        if not coordinates:
            messages.error(request, "Invalid coordinates format.")
            return redirect('raise_complaint')

        try:
            lat, lon = map(float, coordinates.split(','))
        except ValueError:
            messages.error(request, "Invalid coordinates format after normalization.")
            return redirect('raise_complaint')

        # Save the attempted coordinates to the database with detailed debugging
        from .models import UserAttemptedLocation
        try:
            with transaction.atomic():
                attempted_location = UserAttemptedLocation.objects.create(user=user, coordinates=coordinates)
                print(f"Saved attempted location: {attempted_location.coordinates} for {user.email} (ID: {attempted_location.id})")
                db_record = UserAttemptedLocation.objects.filter(id=attempted_location.id).first()
                print(f"Verified database record: {db_record.coordinates if db_record else 'Not found'}")
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM myapp_userattemptedlocation WHERE id = %s", [attempted_location.id])
                    print(f"Raw SQL query result: {cursor.fetchone()}")
                    cursor.execute("""
                        INSERT INTO myapp_userattemptedlocation (user_id, coordinates, timestamp)
                        VALUES (%s, %s, NOW())
                    """, [user.id, coordinates])
                    print(f"Raw SQL insert test result: {cursor.rowcount} rows affected")
        except Exception as e:
            print(f"Error saving attempted location: {str(e)}")
            print(f"User object: {user}")
            print(f"User ID: {user.id}, Email: {user.email}")
            print(f"Coordinates: {coordinates}")
            print(f"Model fields: user={user}, coordinates={coordinates}")
            print(f"Database connection status: {connection.connection}")
            print(f"Transaction state: {transaction.get_autocommit()}")
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    print("Database connection test: Success")
            except Exception as db_error:
                print(f"Database connection error: {str(db_error)}")
            try:
                UserAttemptedLocation.objects.create(
                    user_id=user.id,
                    coordinates=coordinates
                )
                print("Explicit save attempt succeeded with user_id")
            except Exception as explicit_error:
                print(f"Explicit save error: {str(explicit_error)}")

        # Show and associate the nearest complaint (within 300 meters) immediately
        existing_complaints = Complaint.objects.exclude(email=email)
        closest_complaint = None
        min_distance = float('inf')
        for complaint in existing_complaints:
            if complaint.coordinates:
                try:
                    existing_lat, existing_lon = map(float, normalize_coordinates(complaint.coordinates).split(','))
                    distance = haversine(lat, lon, existing_lat, existing_lon)
                    print(f"Checking distance to complaint {complaint.complaint_id}: {distance:.2f} meters")
                    if distance <= 300 and distance < min_distance:
                        min_distance = distance
                        closest_complaint = complaint
                        print(f"Found closer complaint: ID={closest_complaint.complaint_id}, Distance={min_distance:.2f}m")
                except (ValueError, AttributeError):
                    print(f"Error processing coordinates for complaint {complaint.complaint_id}")
                    continue

        # If a nearby complaint is found, associate it with the user permanently
        if closest_complaint and closest_complaint.email != user.email:
            # Check if this complaint is already associated with the user
            if not Complaint.objects.filter(complaint_id=closest_complaint.complaint_id, email=user.email).exists():
                # Create a new complaint record for this user with a new unique complaint_id
                new_complaint_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                while Complaint.objects.filter(complaint_id=new_complaint_id).exists():
                    new_complaint_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                new_complaint = Complaint(
                    complaint_id=new_complaint_id,  # Generate a new unique complaint_id
                    issue_type=closest_complaint.issue_type,
                    severity=closest_complaint.severity,
                    description=f"Associated nearby complaint (Original ID: {closest_complaint.complaint_id})",
                    location=closest_complaint.location,
                    coordinates=closest_complaint.coordinates,
                    image=closest_complaint.image,
                    timestamp=timezone.now(),
                    email=user.email,  # Associate with the current user
                    status=closest_complaint.status,
                    resolved_on=closest_complaint.resolved_on,
                    comment=closest_complaint.comment
                )
                new_complaint.save()
                print(f"Associated nearby complaint with new ID {new_complaint_id} for user {user.email}")
                # Redirect to view_complaint to show the new association
                messages.success(request, f"Associated nearby complaint (ID: {new_complaint_id}) successfully!")
                return redirect('view_complaint')
            else:
                print(f"Complaint {closest_complaint.complaint_id} already associated with user {user.email}")
                complaints.append(Complaint.objects.get(complaint_id=closest_complaint.complaint_id, email=user.email))
        elif closest_complaint:
            complaints.append(closest_complaint)  # Add if already associated

        if 'image' in request.FILES:
            image = request.FILES['image']
            try:
                pil_image = Image.open(image).convert('RGB')
                image_np = np.array(pil_image)
                results = model(image_np)
                names = model.names

                detected_objects = []
                confidence_scores = []
                for box in results[0].boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    detected_objects.append(names[class_id])
                    confidence_scores.append(confidence)

                issue_type_mapping = {
                    "pothole": "pothole",
                    "alligator": "crack",
                    "traversal": "crack",
                    "longitudinal": "crack"
                }

                if detected_objects:
                    max_conf_idx = confidence_scores.index(max(confidence_scores))
                    detected_class = detected_objects[max_conf_idx]
                    issue_type = issue_type_mapping.get(detected_class, "other")
                else:
                    messages.error(request, "No road damage detected.")
                    return redirect('raise_complaint')

                report = Complaint(
                    issue_type=issue_type,
                    severity=severity,
                    description=description,
                    coordinates=coordinates,
                    location=location,
                    email=email,
                )
                report.save()
                print(f"Saved complaint: ID={report.complaint_id}, Email={report.email}")

                fs = FileSystemStorage()
                image_extension = os.path.splitext(image.name)[1]
                image_name = f"{report.complaint_id}{image_extension}"
                image_url = fs.save(image_name, image)
                report.image = image_url
                report.save()
                print(f"Image saved: {image_url}")

                messages.success(request, f"Complaint raised successfully! Detected issue: {issue_type}")
                return redirect('view_complaint')

            except Exception as e:
                messages.error(request, f"Error processing image: {str(e)}")
                return redirect('raise_complaint')
        else:
            messages.error(request, "Please upload an image.")
            return redirect('raise_complaint')

    return render(request, 'raise.html')

def home(request):
    return render(request, 'landingpage.html')


# Function to validate password
def is_valid_password(password):
    return (len(password) >= 8 and 
            re.search(r"\d", password) and 
            re.search(r"[A-Za-z]", password) and 
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

User = get_user_model()

def signup_view(request):
    error_message = None 

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if email is unique
        if CustomUser.objects.filter(email=email).exists():
            error_message = "Email already exists"
            messages.error(request, "Email already exists")
            return render(request, 'signup.html', {
                'first_name': first_name, 
                'last_name': last_name, 
                'email': email, 
                'error_message': error_message
            })

        # Check if passwords match
        if password != confirm_password:
            error_message = "Passwords do not match. Please try again."
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, 'signup.html', {
                'first_name': first_name, 
                'last_name': last_name, 
                'email': email, 
                'error_message': error_message
            })
        
        # Validate password
        if not is_valid_password(password):
            error_message = "Password must be at least 8 characters long and include digits, alphabets, and special characters."
            messages.error(request, error_message)
            return render(request, 'signup.html', {
                'first_name': first_name, 
                'last_name': last_name, 
                'email': email, 
                'error_message': error_message
            })
        
        try:
            # Create the new user
            user = User.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                # The UserProfile will be created automatically via the signal
                
            # Update the last_login time for the profile
            user.userprofile.last_login = timezone.now()
            user.userprofile.save()

            messages.success(request, "Signup successful! Redirecting to login page in 3 seconds...")
            return render(request, 'signup.html', {'redirect': True})
            
        except Exception as e:
            error_message = f"An error occurred during signup: {str(e)}"
            messages.error(request, error_message)
            return render(request, 'signup.html', {
                'first_name': first_name, 
                'last_name': last_name, 
                'email': email, 
                'error_message': error_message
            })

    return render(request, 'signup.html')

def login_view(request):
    error_message = None  # Initialize error message
    email_value = ""  # Default empty email field

    # Check if the user is already authenticated
    
    if request.user.is_authenticated:
        email = request.user.email  # Get the logged-in user's email
        user = request.user
        # Check if the email is in the CustomUser table
        if CustomUser.objects.filter(email=email).exists() and user.is_government_official == 0 :
            request.session['user_id'] = user.id
            return redirect('user_home')  # Redirect to user_home if found in CustomUser

        # Check if the email is in the Employee table
        elif Employee.objects.filter(email=email).exists():
            request.session['user_id'] = user.id
            return redirect('admin_home')  # Redirect to admin_home if in Employee

    # If the user is not authenticated, process the login form
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)


        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)


        # Check if user is valid
        if user is not None and user.is_authenticated:
            login(request, user)

            # Now that user is authenticated, you can check the specific attributes
            if user.is_admin == 1 or user.is_government_official == 1:
                request.session['user_id'] = user.id
                # Proceed with your logic for logged-in government official or admin
                return redirect('admin_home')  # Example redirect
            else:
                request.session['user_id'] = user.id
                return redirect('user_home')  # Redirect for regular users

        else:
            error_message = "Either email or password is incorrect"
            email_value = email  # Retain the email field value

    
    # Render the login page with error message if login failed or not authenticated
    return render(request, 'login.html', {
        'error_message': error_message,
        'email_value': email_value  # Pass email back to the template
    })




def logout_all_sessions(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        
        # Find and delete all sessions associated with the logged-in user
        sessions = Session.objects.all()  # Get all sessions
        
        for session in sessions:
            # Decode session data to check if it belongs to the user
            session_data = session.get_decoded()
            if session_data.get('_auth_user_id') == str(user_id):
                session.delete()  # Delete the session if it matches the user ID
        
        # Now log the user out from the current session
        logout(request)
    
    # Redirect to the home page after logout
    return redirect('home')


@login_required
def profile_settings(request):
    user = request.user  # Assuming CustomUser model is used
    if not user:
        return redirect('login')
    error_message = None

    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        phone = request.POST.get('contact-no')

        # Check if the new email already exists in the database
        if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "Email already exists")
            return redirect('profile_settings')
        
        # Check if the new phone number already exists in the database
        if CustomUser.objects.filter(phone=phone).exclude(id=user.id).exists():
            # error_message = "Phone number already exists"
            messages.error(request, 'Phone number already exists')
            return redirect('profile_settings')
            
        else:
            # Update profile details
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone = phone if phone else None  # Allow empty mobile number
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_settings')

    # Render the page without error_message on GET request
    return render(request, 'profilesetting.html')


@login_required
def change_password(request):
    user = request.user  # Assuming CustomUser model is used\
    if not user:
        return redirect('login')
    current_password = None  # Variable to store current password if it's correct

    if request.method == 'POST':
        current = request.POST.get('current-password')
        new = request.POST.get('new-password')
        c_new = request.POST.get('confirm-password')

        # Check if current password is correct
        if not user.check_password(current):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')

        current_password = current  # Store the correct current password to keep it in the form

        # Check if new password and confirm password match
        if new != c_new:
            messages.error(request, 'New passwords do not match.')
            return render(request, 'change-password.html', {'current_password': current_password})

        # Check if new password is the same as the current password
        if current == new:
            messages.error(request, 'New password cannot be the same as current password.')
            return render(request, 'change-password.html', {'current_password': current_password})
        
        # Validate the strength of the new password
        if not is_valid_password(new):
            messages.error(request, "Password must be at least 8 characters long and include digits, alphabets, and special characters.")
            return render(request, 'change-password.html', {'current_password': current_password})

        try:
            # Set the new password
            user.set_password(new)
            user.save()

            # Update the session to prevent logout after password change
            update_session_auth_hash(request, user)
            
            messages.success(request, 'Password changed successfully.')
            return redirect('change_password')
            
        except Exception as e:
            messages.error(request, 'An error occurred while changing the password. Please try again.')
            return render(request, 'change-password.html', {'current_password': current_password})

    return render(request, 'change-password.html')

# Load the YOLO model once (as a global variable)
model_path = os.path.join(settings.BASE_DIR, 'myapp', 'src', 'ml_model', 'best.pt')
model = YOLO(model_path)

# before nearby raised complaint was working
# @login_required
# def raise_complaint(request):
#     user = request.user
#     if not user:
#         return redirect('login')

#     if request.method == 'POST':
#         # Get form data except issue_type since we'll determine it from the model
#         severity = request.POST.get('severity', '')
#         description = request.POST.get('description', '')
#         coordinates = request.POST.get('coordinates', None)
#         location = request.POST.get('location', '')

#         # Validate required fields
#         if not (severity and coordinates and location):
#             if not coordinates:
#                 messages.error(request, "Please select a location on the map.")
#                 return redirect('raise_complaint')

#             messages.error(request, "All fields are required.")
#             return redirect('raise_complaint')

#         email = user.email

#         if 'image' in request.FILES:
#             image = request.FILES['image']
#             try:
#                 # Convert image for YOLO processing
#                 pil_image = Image.open(image).convert('RGB')
#                 image_np = np.array(pil_image)

#                 # Perform detection
#                 results = model(image_np)
#                 names = model.names
                
#                 # Get detected classes and their confidence scores
#                 detected_objects = []
#                 confidence_scores = []
#                 for box in results[0].boxes:
#                     class_id = int(box.cls[0])
#                     confidence = float(box.conf[0])
#                     detected_objects.append(names[class_id])
#                     confidence_scores.append(confidence)

#                 # Map detected classes to issue types
#                 issue_type_mapping = {
#                     "pothole": "pothole",
#                     "alligator": "crack",
#                     "traversal": "crack",
#                     "longitudinal": "crack"
#                 }

#                 # Determine issue type based on detection with highest confidence
#                 if detected_objects:
#                     max_conf_idx = confidence_scores.index(max(confidence_scores))
#                     detected_class = detected_objects[max_conf_idx]
#                     issue_type = issue_type_mapping.get(detected_class, "other")
#                 else:
#                     messages.error(request, "No road damage detected. Complaint not registered.")
#                     return redirect('raise_complaint')

#                 # Create and save the complaint with detected issue_type
#                 report = Complaint(
#                     issue_type=issue_type,
#                     severity=severity,
#                     description=description,
#                     coordinates=coordinates,
#                     location=location,
#                     email=email,
#                 )
#                 report.save()

#                 # Save the image
#                 fs = FileSystemStorage()
#                 image_extension = os.path.splitext(image.name)[1]
#                 image_name = f"{report.complaint_id}{image_extension}"
#                 image_url = fs.save(image_name, image)
#                 report.image = image_url
#                 report.save()

#                 messages.success(request, f"Complaint raised successfully! Detected issue: {issue_type}")
#                 return redirect('raise_complaint')

#             except Exception as e:
#                 messages.error(request, f"An error occurred while processing the image: {str(e)}")
#                 return redirect('raise_complaint')

#         else:
#             messages.error(request, "Please upload an image for analysis.")
#             return redirect('raise_complaint')

#     return render(request, 'raise.html')


# after nearby raised complaint working
from math import radians, sin, cos, sqrt, atan2

@login_required
def raise_complaint(request):
    user = request.user
    if not user:
        return redirect('login')

    # Haversine formula to calculate distance between two points (in meters)
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # Earth's radius in meters
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c

    if request.method == 'POST':
        severity = request.POST.get('severity', '')
        description = request.POST.get('description', '')
        coordinates = request.POST.get('coordinates', None)
        location = request.POST.get('location', '')

        # Validate required fields
        if not (severity and coordinates and location):
            if not coordinates:
                messages.error(request, "Please select a location on the map.")
            else:
                messages.error(request, "All fields are required.")
            return redirect('raise_complaint')

        email = user.email
        lat, lon = map(float, coordinates.split(','))

        # Check for existing complaints within 300 meters
        existing_complaints = Complaint.objects.all()
        for complaint in existing_complaints:
            if complaint.coordinates:
                try:
                    existing_lat, existing_lon = map(float, complaint.coordinates.split(','))
                    distance = haversine(lat, lon, existing_lat, existing_lon)
                    if distance <= 300:  # 300 meters buffer
                        messages.info(request, f"A similar complaint already exists at this location (Complaint ID: {complaint.complaint_id}). It will be visible in your complaint list.")
                        return redirect('raise_complaint')
                except (ValueError, AttributeError):
                    continue  # Skip invalid coordinates

        # If no nearby complaint exists, process the new complaint
        if 'image' in request.FILES:
            image = request.FILES['image']
            try:
                pil_image = Image.open(image).convert('RGB')
                image_np = np.array(pil_image)
                results = model(image_np)
                names = model.names
                
                detected_objects = []
                confidence_scores = []
                for box in results[0].boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    detected_objects.append(names[class_id])
                    confidence_scores.append(confidence)

                issue_type_mapping = {
                    "pothole": "pothole",
                    "alligator": "crack",
                    "traversal": "crack",
                    "longitudinal": "crack"
                }

                if detected_objects:
                    max_conf_idx = confidence_scores.index(max(confidence_scores))
                    detected_class = detected_objects[max_conf_idx]
                    issue_type = issue_type_mapping.get(detected_class, "other")
                else:
                    messages.error(request, "No road damage detected. Complaint not registered.")
                    return redirect('raise_complaint')

                # Save the new complaint
                report = Complaint(
                    issue_type=issue_type,
                    severity=severity,
                    description=description,
                    coordinates=coordinates,
                    location=location,
                    email=email,
                )
                report.save()

                fs = FileSystemStorage()
                image_extension = os.path.splitext(image.name)[1]
                image_name = f"{report.complaint_id}{image_extension}"
                image_url = fs.save(image_name, image)
                report.image = image_url
                report.save()

                messages.success(request, f"Complaint raised successfully! Detected issue: {issue_type}")
                return redirect('raise_complaint')

            except Exception as e:
                messages.error(request, f"An error occurred while processing the image: {str(e)}")
                return redirect('raise_complaint')
        else:
            messages.error(request, "Please upload an image for analysis.")
            return redirect('raise_complaint')

    return render(request, 'raise.html')

# @login_required
# def raise_complaint(request):
#     user = request.user
#     if not user:
#         return redirect('login')

#     if request.method == 'POST':
#         issue_type = request.POST.get('issue_type', '')
#         severity = request.POST.get('severity', '')
#         description = request.POST.get('description', '')
#         coordinates = request.POST.get('coordinates', None)
#         location = request.POST.get('location', '')

#         # Validate required fields
#         if not (issue_type and severity and coordinates):
#             messages.error(request, "All fields are required.")
#             return redirect('raise_complaint')

#         email = user.email

#         # Handle image upload and run YOLO detection
#         if 'image' in request.FILES or request.POST.get('camera_image'):
#             # Get image either from file upload or camera capture
#             image = request.FILES.get('image') or request.POST.get('camera_image')
            
#             try:
#                 # Convert image to format suitable for YOLO processing
#                 if isinstance(image, str):  # If it's a base64 string from camera
#                     import base64
#                     from io import BytesIO
#                     # Remove the data URL prefix
#                     image_data = image.split(',')[1]
#                     image = BytesIO(base64.b64decode(image_data))
                
#                 pil_image = Image.open(image).convert('RGB')
#                 image_np = np.array(pil_image)

#                 # Perform detection
#                 results = model(image_np)
#                 names = model.names
#                 detected_classes = [names[int(box.cls[0])] for box in results[0].boxes]

#                 crack_classes = ["pothole", "alligator", "traversal", "longitudinal"]
#                 is_crack_detected = any(cls in crack_classes for cls in detected_classes)

#                 if not is_crack_detected:
#                     messages.error(request, "No cracks or potholes detected. Complaint not registered.")
#                     return redirect('raise_complaint')

#                 # Save the complaint
#                 report = Complaint(
#                     issue_type=issue_type,
#                     severity=severity,
#                     description=description,
#                     coordinates=coordinates,
#                     location=location,
#                     email=email,
#                 )
#                 report.save()

#                 # Save the image
#                 fs = FileSystemStorage()
#                 if isinstance(image, BytesIO):  # If it's from camera
#                     image_name = f"{report.complaint_id}.png"
#                     image_content = ContentFile(image.getvalue())
#                     image_url = fs.save(image_name, image_content)
#                 else:  # If it's from file upload
#                     image_extension = os.path.splitext(image.name)[1]
#                     image_name = f"{report.complaint_id}{image_extension}"
#                     image_url = fs.save(image_name, image)

#                 report.image = image_url
#                 report.save()

#                 messages.success(request, "Complaint raised successfully!")
#                 return redirect('raise_complaint')

#             except Exception as e:
#                 messages.error(request, f"An error occurred while processing the image: {str(e)}")
#                 return redirect('raise_complaint')

#         else:
#             messages.error(request, "Please provide an image either by uploading or capturing with camera.")
#             return redirect('raise_complaint')

#     return render(request, 'raise.html')



def forgot_password(request):
    return render(request, 'forgot-password.html')

#User-view
@login_required
def user_home(request):
    user = request.user
    if not user:
        return redirect('login')
    return render(request, 'user.html')

#before nearby raised compliants was working
# @login_required
# def view_complaint(request):
#     user = request.user
#     if not user:
#         return redirect('login')
#     status_filter = request.GET.get('statusFilter', 'all')
#     sort_filter = request.GET.get('sortFilter', 'newest')

#     # Get the logged-in user's email
#     user_email = request.user.email  # Assuming the user is logged in
    
#     # Filter complaints where the email matches the logged-in user's email
#     complaints = Complaint.objects.filter(email=user_email)

#     # Filter by status if it's not 'all'
#     if status_filter != 'all':
#         complaints = complaints.filter(status=status_filter)

#     # Sort by date based on the user's choice
#     if sort_filter == 'oldest':
#         complaints = complaints.order_by('timestamp')
#     else:
#         complaints = complaints.order_by('-timestamp')

#     context = {
#         'complaints': complaints,
#     }
#     return render(request, 'complaint.html', context)

#after nearby raised complaints working
# @login_required
# def view_complaint(request):
#     user = request.user
#     if not user:
#         return redirect('login')

#     # Haversine formula to calculate distance between two points (in meters)
#     def haversine(lat1, lon1, lat2, lon2):
#         R = 6371000  # Earth's radius in meters
#         lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
#         dlat = lat2 - lat1
#         dlon = lon2 - lon1
#         a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#         c = 2 * atan2(sqrt(a), sqrt(1-a))
#         return R * c

#     status_filter = request.GET.get('statusFilter', 'all')
#     sort_filter = request.GET.get('sortFilter', 'newest')

#     # Get complaints raised by the user
#     user_complaints = Complaint.objects.filter(email=user.email)

#     # Find nearby complaints (within 300 meters) raised by others
#     all_complaints = Complaint.objects.exclude(email=user.email)  # Exclude user's own complaints
#     nearby_complaints = []
#     for user_complaint in user_complaints:
#         if user_complaint.coordinates:
#             try:
#                 user_lat, user_lon = map(float, user_complaint.coordinates.split(','))
#                 for complaint in all_complaints:
#                     if complaint.coordinates:
#                         try:
#                             other_lat, other_lon = map(float, complaint.coordinates.split(','))
#                             distance = haversine(user_lat, user_lon, other_lat, other_lon)
#                             if distance <= 300 and complaint not in nearby_complaints:
#                                 nearby_complaints.append(complaint)
#                         except (ValueError, AttributeError):
#                             continue
#             except (ValueError, AttributeError):
#                 continue

#     # Combine user's complaints with nearby complaints
#     complaints = list(user_complaints) + nearby_complaints

#     # Apply filters
#     if status_filter != 'all':
#         complaints = [c for c in complaints if c.status == status_filter]

#     # Sort by date
#     if sort_filter == 'oldest':
#         complaints.sort(key=lambda x: x.timestamp)
#     else:
#         complaints.sort(key=lambda x: x.timestamp, reverse=True)

#     context = {
#         'complaints': complaints,
#     }
#     return render(request, 'complaint.html', context)

from math import radians, sin, cos, sqrt, atan2
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint
from django.http import HttpRequest
@login_required
def view_complaint(request):
    user = request.user
    if not user:
        return redirect('login')

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # Earth's radius in meters
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def normalize_coordinates(coord_str):
        try:
            lat, lon = map(float, coord_str.split(','))
            lat = round(lat, 6)  # Round to 6 decimal places (~1 meter precision)
            lon = round(lon, 6)
            return f"{lat},{lon}"
        except ValueError:
            return None

    status_filter = request.GET.get('statusFilter', 'all')
    sort_filter = request.GET.get('sortFilter', 'newest')

    # Get complaints raised by the user
    user_complaints = Complaint.objects.filter(email=user.email)
    print(f"User complaints: {len(user_complaints)} found for {user.email}")
    for complaint in user_complaints:
        print(f" - ID: {complaint.complaint_id}, Status: {complaint.status}, Coordinates: {complaint.coordinates}")

    # Initialize list of complaints to display
    complaints = list(user_complaints)
    all_complaints = Complaint.objects.exclude(email=user.email)  # Exclude user's own complaints
    closest_complaint = None
    min_distance = float('inf')

    # Try to use POST data or GET params as a fallback if database fails
    coordinates = request.POST.get('coordinates') or request.GET.get('coordinates')
    if not coordinates:
        from .models import UserAttemptedLocation
        latest_attempt = UserAttemptedLocation.objects.filter(user=user).order_by('-timestamp').first()
        if latest_attempt:
            coordinates = latest_attempt.coordinates
    else:
        coordinates = normalize_coordinates(coordinates)

    if coordinates:
        try:
            user_lat, user_lon = map(float, coordinates.split(','))
            print(f"Using coordinates from POST/GET or DB: {coordinates}")
            for complaint in all_complaints:
                if complaint.coordinates:
                    try:
                        normalized_coords = normalize_coordinates(complaint.coordinates)
                        if normalized_coords:
                            other_lat, other_lon = map(float, normalized_coords.split(','))
                            distance = haversine(user_lat, user_lon, other_lat, other_lon)
                            print(f"Checking distance to complaint {complaint.complaint_id}: {distance:.2f} meters")
                            if distance <= 300 and distance < min_distance:
                                min_distance = distance
                                closest_complaint = complaint
                                print(f"Found closer complaint: ID={closest_complaint.complaint_id}, Distance={min_distance:.2f}m")
                    except (ValueError, AttributeError):
                        print(f"Error processing coordinates for complaint {complaint.complaint_id}")
                        continue
        except (ValueError, AttributeError):
            print("Invalid coordinates from POST/GET or DB")
    else:
        print("No coordinates available for nearby search")

    # Add the closest nearby complaint if found (for display only, no database save)
    if closest_complaint and closest_complaint not in complaints:  # Avoid duplicates
        complaints.append(closest_complaint)
        print(f"Closest complaint added for display: ID={closest_complaint.complaint_id}, Distance={min_distance:.2f}m")

    # If user has complaints, also check nearby complaints based on their complaint locations
    if user_complaints:
        for user_complaint in user_complaints:
            if user_complaint.coordinates:
                try:
                    user_lat, user_lon = map(float, normalize_coordinates(user_complaint.coordinates).split(','))
                    for complaint in all_complaints:
                        if complaint.coordinates:
                            try:
                                other_lat, other_lon = map(float, normalize_coordinates(complaint.coordinates).split(','))
                                distance = haversine(user_lat, user_lon, other_lat, other_lon)
                                print(f"Checking distance to complaint {complaint.complaint_id}: {distance:.2f} meters")
                                if distance <= 300 and distance < min_distance:
                                    min_distance = distance
                                    closest_complaint = complaint
                                    print(f"Found closer complaint: ID={closest_complaint.complaint_id}, Distance={min_distance:.2f}m")
                            except (ValueError, AttributeError):
                                print(f"Error processing coordinates for complaint {complaint.complaint_id}")
                                continue
                except (ValueError, AttributeError):
                    print(f"Invalid coordinates for user complaint {user_complaint.complaint_id}")

    # Add the closest nearby complaint if found (from user complaints check, for display only)
    if closest_complaint and closest_complaint not in complaints:  # Avoid duplicates
        complaints.append(closest_complaint)
        print(f"Closest complaint added for display: ID={closest_complaint.complaint_id}, Distance={min_distance:.2f}m")

    print(f"Total complaints before filtering: {len(complaints)}")

    # Apply status filter
    if status_filter != 'all':
        complaints = [c for c in complaints if c.status == status_filter]
        print(f"After status filter ({status_filter}): {len(complaints)}")

    # Apply search filter if provided
    if request.GET.get('search'):
        search_query = request.GET.get('search').lower()
        complaints = [c for c in complaints if search_query in c.complaint_id.lower() or search_query in c.issue_type.lower() or search_query in c.location.lower()]
        print(f"After search filter: {len(complaints)}")

    # Sort by date
    if sort_filter == 'oldest':
        complaints.sort(key=lambda x: x.timestamp)
    else:
        complaints.sort(key=lambda x: x.timestamp, reverse=True)

    context = {
        'complaints': complaints,
    }
    print(f"Context complaints: {len(context['complaints'])}")
    return render(request, 'complaint.html', context)

@login_required
def delete_complaint(request, complaint_id):
    user = request.user
    if not user:
        return redirect('login')
    error_message = None

    print(f"Request received to delete complaint ID: {complaint_id}")
    if Complaint.objects.filter(complaint_id = complaint_id).exists():
        # Fetch the complaint for the logged-in user and delete it if it exists
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id, email=user.email)
        # Delete the complaint
        complaint.delete()
        messages.success(request, "Complaint Successfully Deleted")
    else:
        messages.error(request, "Error while deleting the complaint")
    
    # Redirect back to the complaint list page after deletion
    return redirect('view_complaint')

@login_required
def view_map(request):
    user = request.user
    if not user:
        return redirect('login')
    return render(request, 'map.html')

@login_required
def get_complaints(request):
    user = request.user
    if not user:
        return redirect('login')
    complaints = Complaint.objects.all()
    complaints_data = []
    
    for complaint in complaints:
        if complaint.coordinates:
            try:
                lat, lng = map(float, complaint.coordinates.split(','))
                complaint_data = {
                    'location': {
                        'lat': lat,
                        'lng': lng
                    },
                    'status': complaint.status,
                    'issueType': complaint.issue_type,
                    'severity': complaint.severity,
                    'date': complaint.timestamp.strftime('%d-%m-%Y'),
                    'description': complaint.description,
                    'imageUrl': complaint.image.url if complaint.image else None,
                }
                complaints_data.append(complaint_data)
            except (ValueError, AttributeError):
                # Skip complaints with invalid coordinates
                continue
    
    return JsonResponse(complaints_data, safe=False)


#Admin-view
@login_required
def admin_report(request):
    user = request.user
    if not user:
        return redirect('login')
    return render(request, 'admin-report-dashboard.html')

@login_required
def admin_profile_settings(request):
    user=request.user # Assuming CustomUser model is used
    if not user:
        return redirect('login')
    
    error_message = None

    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        phone = request.POST.get('contact-no')

        # Check if the new email already exists in the database
        if Employee.objects.filter(email=email).exclude(id=user.id).exists():
            # error_message = "Email already exists"
            messages.error(request, "Email already exists")
            return redirect('admin_profile_settings')
        
        # Check if the new phone number already exists in the database
        if Employee.objects.filter(phone=phone).exclude(id=user.id).exists():
            messages.error(request, 'Phone number already exists')
            return redirect('admin_profile_settings')
        
        else:
            # Update profile details
            user.first_name = first_name
            user.last_name = last_name
            # user.email = email
            user.phone = phone if phone else None  # Allow empty mobile number
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('admin_profile_settings')

    # Render the page without error_message on GET request
    return render(request, 'admin-setting.html')

@login_required
def admin_change_password(request):
    user=request.user # Assuming CustomUser model is used
    if not user:
        return redirect('login')
    
    current_password = None  # Variable to store current password if it's correct

    if request.method == 'POST':
        current = request.POST.get('current-password')
        new = request.POST.get('new-password')
        c_new = request.POST.get('confirm-password')

        # Check if current password is correct
        if not user.check_password(current):
            messages.error(request, 'Current password is incorrect.')
            return redirect('admin_change_password')

        current_password = current  # Store the correct current password to keep it in the form

        # Check if new password and confirm password match
        if new != c_new:
            messages.error(request, 'New passwords do not match.')
            return render(request, 'admin-change-password.html', {'current_password': current_password})

        # Check if new password is the same as the current password
        if current == new:
            messages.error(request, 'New password cannot be the same as current password.')
            return render(request, 'admin-change-password.html', {'current_password': current_password})
        
        # Validate the strength of the new password
        if not is_valid_password(new):
            messages.error(request, "Password must be at least 8 characters long and include digits, alphabets, and special characters.")
            return render(request, 'admin-change-password.html', {'current_password': current_password})

        try:
            # Set the new password
            user.set_password(new)
            user.save()

            # Update the session to prevent logout after password change
            update_session_auth_hash(request, user)
            
            messages.success(request, 'Password changed successfully.')
            return redirect('admin_change_password')
            
        except Exception as e:
            messages.error(request, 'An error occurred while changing the password. Please try again.')
            return render(request, 'admin-change-password.html', {'current_password': current_password})

    return render(request, 'admin-change-password.html')

@login_required
def admin_map(request):
    user=request.user
    if not user:
        return redirect('login')
    return render(request, 'admin-map.html')


@login_required
def admin_setting(request): 
    user=request.user
    if not user:
        return redirect('login')
    if request.method == 'POST':   
        employees = Employee.objects.all()
    
        employee_id = request.POST.get('employee')
        role = request.POST.get('role')
        # You can assign the role to the selected employee here, or log the activity.
    return render(request, 'admin-role.html', {'employees': employees})
    
@login_required
def admin_home(request):
    user=request.user
    if not user:
        return redirect('login')
    return render(request, 'admin-home.html')

# View to display all employees
@login_required
def employee_list(request):
    user=request.user
    if not user:
        return redirect('login')
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

@login_required
def delete_employee(request, emp_id, email):
    user = request.user
    if not user:
        return redirect('login')
    error_message = None

    if Employee.objects.filter(emp_id = emp_id).exists() and CustomUser.objects.filter(email = email).exists():
        employee = get_object_or_404(Employee, emp_id=emp_id)
        # Delete the employee
        employee.delete()
        customuser = get_object_or_404(CustomUser, email=email)
        customuser.delete()
        messages.success(request, "Employee Successfully Deleted")
    else:
        messages.error(request, "Error while deleting the complaint")
    
    # Redirect back to the complaint list page after deletion
    return redirect('employee_list')


# View to assign a task to an employee
@login_required
def assign_task(request):
    user=request.user
    if not user:
        return redirect('login')
    if request.method == 'POST':
        # Get data from the form
        employee_id = request.POST.get('employee')
        task_type = request.POST.get('task_type')
        description = request.POST.get('description')
        complaint_id = request.POST.get('complaint_id', None)
        
        employee = Employee.objects.get(id=employee_id)
        complaint = Complaint.objects.get(id=complaint_id) if complaint_id else None

        # Create a new task
        task = Task(
            task_type=task_type,
            description=description,
            assigned_employee=employee,
            complaint=complaint
        )
        task.save()

        # Show success message
        messages.success(request, f"Task '{task.get_task_type_display()}' assigned to {employee.first_name}.")
        return redirect('assign_task')

    employees = Employee.objects.all()
    tasks = Task.TASK_TYPE_CHOICES  # All task types to choose from
    return render(request, 'assign_task.html', {'employees': employees, 'tasks': tasks})


# View for adding a new employee
@login_required
def add_employee(request):
    user=request.user
    if not user:
        return redirect('login')
    elif request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()  # Save the employee record to the database
            messages.success(request, 'Employee added successfully!')
            return redirect('add_employee')  # Redirect to employee list page
        else:
            messages.error(request, 'Error adding employee. Please check the form.')
    else:
        form = EmployeeForm()

    return render(request, 'add_employee.html', {'form': form})

@login_required
def update_complaint_status(request, complaint_id):
    user=request.user
    if not user:
        return redirect('login')
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        status = request.POST['status']
        comment = request.POST['comment']

        complaint.status = status
        complaint.comment = comment
        complaint.resolved_on = timezone.now().strftime('%d-%m-%Y')
        complaint.save()
        
        messages.success(request, 'Complaint status updated successfully.')
        return redirect('complaint_list')

    return render(request, 'update_complaint_status.html', {'complaint': complaint})

@login_required
def complaint_list(request):
    user=request.user
    if not user:
        return redirect('login')
    complaints = Complaint.objects.all()
    return render(request, 'complaint_list.html', {'complaints': complaints})

# # View to generate a report (for example, a list of complaints with their status)
# @login_required
# def generate_report(request):
#     user=request.user
#     if not user:
#         return redirect('login')
#     complaints = Complaint.objects.all()
#     if request.method == 'POST':
#         # Generate the report (could be PDF, CSV, etc.)
#         report_type = request.POST.get('report_type')

#         if report_type == 'pdf':
#             # Example for PDF (you can use libraries like ReportLab to generate PDFs)
#             # Here you could return a PDF response with the complaints data
#             pass

#         elif report_type == 'csv':
#             # Generate CSV (you can use Python's CSV library)
#             # Example:
#             import csv
#             from django.http import HttpResponse

#             response = HttpResponse(content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="complaints_report.csv"'
#             writer = csv.writer(response)
#             writer.writerow(['Complaint ID', 'Issue Type', 'Severity', 'Status', 'Location'])

#             for complaint in complaints:
#                 writer.writerow([complaint.complaint_id, complaint.issue_type, complaint.severity, complaint.status, complaint.location])

#             return response

#         messages.success(request, "Report generated successfully!")
#         return redirect('complaint_list')
    
#     return render(request, 'generate_report.html', {'complaints': complaints})



@login_required
def generate_report(request):
    complaints = Complaint.objects.all()
    context = {
        'complaints': complaints,
        'total_complaints': complaints.count(),
        'pending_complaints': complaints.filter(status='Pending').count(),
        'in_progress_complaints': complaints.filter(status='In Progress').count(),
        'resolved_complaints': complaints.filter(status='Resolved').count(),
    }
    return render(request, 'admin-report.html', context)

