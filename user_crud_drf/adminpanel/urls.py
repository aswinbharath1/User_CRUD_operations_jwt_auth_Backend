from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('',views.UserView.as_view() ),
    path('updateuser', views.UserUpdateView.as_view() ),
    path('deleteuser', views.UserUpdateView.as_view() ),
]
