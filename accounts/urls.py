from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    RegisterView,
    LoginView
)

urlpatterns = [
    # 🔹 Template (UI) routes
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # 🔹 API routes (optional, for later use)
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', LoginView.as_view(), name='api_login'),
]