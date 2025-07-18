from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sets/<int:set_id>/alterFlashcard/<int:flashcard_id>", views.alterFlashcard, name="alterFlashcard"),
    path("sets/alterSet/<int:set_id>", views.alterSet, name="alterSet"),
    path("sets/<int:set_id>/createFlashcard", views.createFlashcard, name="createFlashcard"),
    path("createSet", views.createSet, name="createSet"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("saved", views.saved, name="saved"),
    path("sets/<int:set_id>", views.set_view, name="set"),
]
