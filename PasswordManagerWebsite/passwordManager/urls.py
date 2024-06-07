from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("set_masterpass", views.set_master_pass, name="masterpassword"),
    path("get_password/<str:website_name>", views.get_password, name="get_password"),
    path("create_password", views.set_password, name="create_password"),
]
