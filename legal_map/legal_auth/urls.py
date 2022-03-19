from django.urls import path
from legal_map.legal_auth import views

urlpatterns = (
    path('sign-up/', views.SignUpView.as_view(), name='sign up'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('sign-out/', views.sign_out, name='sign out'),
)