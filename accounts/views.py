from django.shortcuts import render
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from .forms import UserLoginForm, UserRegistrationForm
from django.shortcuts import redirect
# Create your views here.

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        login(request, user)
        return redirect("posts:post_list")
    args = {
        'form' : form,
        'title' : "Login",
    }
    return render(request, 'accounts/user_form.html', args )

def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username = username , password = password)
        login(request, new_user)
        return redirect("posts:post_list")
        

    args = {
        'form' : form,
        'title' : "Register",
    }
    return render(request, 'accounts/user_form.html', args)

def logout_view(request):
    logout(request)
    return redirect("accounts:login")