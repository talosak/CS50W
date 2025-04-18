
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page_id>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/<int:user_id>/<int:page_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("following/<int:page_id>", views.following, name="following"),

    # API Routes
    path("posts", views.posts, name="posts"),
    path("paginate", views.paginate, name="paginate"),
    path("like", views.like, name="like"),
    path("unlike", views.unlike, name="unlike"),
]
