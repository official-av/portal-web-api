from django.conf.urls import url
from .views import  AuthRegister,Update,Profile,OtpRegister,CreateQuestion,checkPassword,checkUsername,Invitation
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token


urlpatterns=[
  url(r'^login/',obtain_jwt_token),
  url(r'^verify/',verify_jwt_token),
  url(r'^register/$', AuthRegister.as_view()),
  url(r'^update/$', Update.as_view()),
  url(r'^otp/$',OtpRegister.as_view()),
  url(r'^create/',CreateQuestion.as_view()),
  url(r'^viewprofile/(?P<username>[A-Za-z0-9]+)/$', Profile.as_view()),
  url(r'^check/$',checkPassword.as_view()),
  url(r'^username/$',checkUsername.as_view()),
  url(r'^invite/$',Invitation.as_view()),
]
