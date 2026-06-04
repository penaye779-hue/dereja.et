from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import User
from .serializers import UserSerializer
from .forms import RegisterForm


# =========================
# 🔹 API VIEWS (JSON)
# =========================

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            return Response({
                "message": "Login successful",
                "user_id": user.id,
                "role": user.role
            })
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )


# =========================
# 🔹 TEMPLATE VIEWS (HTML)
# =========================

def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')