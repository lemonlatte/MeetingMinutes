from django.shortcuts import HttpResponse, redirect
from django.contrib import auth


def login(request):

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return redirect("home")
    else:
        return HttpResponse("Login Failed.", content_type="application/json")


def logout(request):

    auth.logout(request)
    return redirect("home")
