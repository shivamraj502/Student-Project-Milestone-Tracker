from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("auth-selection/", views.auth_selection, name="auth_selection"),
    path("login/<str:role>/", views.role_login, name="role_login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register_project, name="register"),
    path("allot/<int:pk>/", views.allot_guide, name="allot"),
    path("upload/", views.upload_milestone, name="upload"),
    path("evaluate/", views.evaluate_project, name="evaluate"),
    path("projects-list/", views.project_list, name="projects_list"),
    path("export/", views.export_projects_csv, name="export_csv"),
]
