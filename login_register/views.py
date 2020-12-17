from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User

def index(request):
  if "user_id" in request.session:
    return redirect(reverse("book:index"))
  return render(request, "login_register/index.html")

def register(request):
  if request.method == "POST":
    res = User.objects.reg_validate(request.POST)
    if res["is_valid"]:
      request.session["user_id"] = res["result"]
      return redirect(reverse("book:index"))
    errors = res["result"].values()
    for error in errors:
      messages.error(request, error)
  return redirect(reverse("user:index"))
    
def login(request):
  if request.method == "POST":
    res = User.objects.login_validate(request.POST)
    if res["is_valid"]:
      request.session["user_id"] = res["result"]
      return redirect(reverse("book:index")) 
    messages.error(request, res["result"])
  return redirect(reverse("user:index"))

