from django.urls import path

from users.views import (
    SignUpUserView,
    SignUpAdminView
)

urlpatterns = [
    path('/signup/general', SignUpUserView.as_view()),
    path('/signup/admin', SignUpAdminView.as_view())
]
