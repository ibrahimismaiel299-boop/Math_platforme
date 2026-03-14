from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import StudentSignupForm

class SignUpView(generic.CreateView):
    form_class = StudentSignupForm
    success_url = reverse_lazy('login') # بعد التسجيل يذهب لصفحة الدخول
    template_name = 'registration/signup.html'

# Create your views here.
