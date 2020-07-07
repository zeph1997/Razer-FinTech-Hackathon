from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.login,name="login"),
    path("register",views.register,name="register"),
    path("buttons",views.buttons,name="buttons"), 
    path("requestcards",views.get_cards,name="requestcards"),
    path("requestimg",views.get_image_resource,name="requestimg"),
    path("index",views.index,name="home"),
    path("cards",views.cards,name="cards")
]