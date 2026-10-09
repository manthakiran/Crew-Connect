from django.urls import path

from hr import views

urlpatterns = [
    path('',views.login_view,name='login'),
    path("dashboard/",views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    # path("viewemployees/", viewemployees, name="viewemployees"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employees_create/", views.employee_create, name="employee_create"),
    path("employees/<int:id>/edit/", views.employee_update, name="employee_update"),
    path("employees/<int:id>/delete/", views.employee_delete, name="employee_delete"),
    path("leave_approval/", views.leave_approval, name="leave_approval"),
    path("leave/<int:id>/action/", views.leave_action, name="leave_action"),
    path("department_create/", views.department_create, name="department_create"),
    path("department_list/", views.department_list, name="department_list"),
    path('departments/<int:id>/edit/', views.department_edit, name='department_edit'),
    path('departments/<int:id>/delete/', views.department_delete, name='department_delete'),
    path('designations_list/',views.designations_list,name='designations_list'),
    path('designations_create/',views.designations_create,name='designations_create'),
    path('designation/<int:id>/delete/', views.designation_delete, name='designation_delete'),
    path('designation/<int:id>/edit/', views.designation_edit, name='designation_edit'),

]