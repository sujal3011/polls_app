from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("",views.index,name="home"),
    path("user_polls",views. userPolls,name="userPolls"),
    path("create",views.create,name="create"),
    path("vote/<poll_id>",views.vote,name="vote"),
    path("result/<poll_id>",views.result,name="result"),
    path("delete/<poll_id>",views.deletePoll,name="deletePoll"),
    path("signup",views.createUser,name="signup"),
    path("login",views.loginUser,name="login"),
    path("logout",views.logoutUser,name="logout")
]