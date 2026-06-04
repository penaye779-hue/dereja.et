from django.urls import path
from .views import ApplyToJobView

urlpatterns = [
    path('apply/', ApplyToJobView.as_view()),
]