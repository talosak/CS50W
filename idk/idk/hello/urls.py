from django.urls import path

from . import views

app_name = "hello"
urlpatterns = [
    path("", views.index, name="index"),
    path("brian", views.brian, name="brian"),
    path("david", views.david, name="david"),
    path("<str:name>", views.greet, name="greet")
]