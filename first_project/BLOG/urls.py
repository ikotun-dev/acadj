from django.urls import path
from . import views 



urlpatterns = [
    path("test-api", views.Test.as_view()),
    path("signup", views.Signup.as_view()),
    path("login", views.Login.as_view()),
    path("create-post", views.Post.as_view()),
    path("toogle-post", views.SearchPost.as_view()),
    path("hirer-signup", views.HirerSignup.as_view()),
    path("hirer-login", views.HirerLogin.as_view()),
    path("freelancer-signup", views.FreelancerSignup.as_view()),
    path("freelancer-login", views.FreelancerLogin.as_view()),
    path("create-job", views.CreateJob.as_view())
]




