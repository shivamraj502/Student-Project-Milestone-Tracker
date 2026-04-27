from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_project, name="register"),
    path("allot/<int:pk>/", views.allot_guide, name="allot"),
    path("upload/", views.upload_milestone, name="upload"),
    path("evaluate/", views.evaluate_project, name="evaluate"),
]
