from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout")
]