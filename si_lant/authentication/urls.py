from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('logout/', LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('logout/', LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),
]
