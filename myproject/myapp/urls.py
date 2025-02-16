# myapp/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # General views
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),


    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_all_sessions, name = 'logout'),
    
    # User views
    path('user/', views.user_home, name='user_home'),
    path('user/raise-complaint/', views.raise_complaint, name='raise_complaint'),
    path('user/view-complaint/', views.view_complaint, name='view_complaint'),
    path('user/view-map/', views.view_map, name='view_map'),
    path('user/view-map/complaints/', views.get_complaints, name='get_complaints'),
    path('user/profile/', views.profile_settings, name='profile_settings'),
    path('user/change_password/', views.change_password, name='change_password'),


    # Admin views
    path('adminhome/', views.admin_home, name = 'admin_home'),
    path('adminhome/profile/', views.admin_profile_settings, name='admin_profile_settings'),
    path('adminhome/change_password/', views.admin_change_password, name='admin_change_password'),

    path('add_employee/', views.add_employee, name='add_employee'),
    path('employee_list/', views.employee_list, name='employee_list'),
    # path('delete_employee/<int:emp_id><str:email>/', views.delete_employee, name='delete_employee'),
    # path('delete_employee/<int:emp_id><str:email>/', views.delete_employee, name='delete_employee'),  # Show confirmation
    # path('confirm_delete_employee/<int:emp_id><str:email>/', views.confirm_delete_employee, name='confirm_delete_employee'),  # Perform deletion
     path('delete_employee/<int:emp_id><str:email>/', views.delete_employee, name='delete_employee'),

    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/<int:complaint_id>/update/', views.update_complaint_status, name='update_complaint_status'),
    path('delete_complaint/<str:complaint_id>/', views.delete_complaint, name='delete_complaint'),

    path('adminhome/map/', views.admin_map, name='admin_map'),
    path('adminhome/map/complaints/', views.get_complaints, name='get_complaints'),
    path('adminhome/report/', views.admin_report, name='admin_report'),
    path('adminhome/settings/', views.admin_setting, name='admin_setting'),
    path('assign_task/', views.assign_task, name='assign_task'),
    path('generate_report/', views.generate_report, name='generate_report'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
