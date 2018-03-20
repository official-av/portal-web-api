from django.conf.urls import url
from .views import  AuthRegister
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns=[
  url(r'^login/',obtain_jwt_token),
  url(r'^register/$', AuthRegister.as_view()),
]
