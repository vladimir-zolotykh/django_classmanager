from django.urls import path
from . import views

urlpatterns = [
    path("", views.define_class, name="define_class"),
    path("update/", views.update_instance, name="update_instance"),
    path("view/", views.view_instance, name="view_instance"),
]
