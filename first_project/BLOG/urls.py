from django.urls import path
from . import views 



urlpatterns = [
    path("test-api", views.Test.as_view()),
    path("signup", views.Signup.as_view()),
    path("login", views.Login.as_view()),
    path("create-post", views.Post.as_view())

]


