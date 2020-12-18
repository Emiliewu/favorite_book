from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Case, When, BooleanField

from .models import Book
from login_register.models import User

def index(request):
  if "user_id" not in request.session:
    return redirect(reverse("user:index"))
  user = User.objects.get(id=request.session["user_id"])
  username = user.first_name
  books = Book.objects.annotate(
    is_favorite=Case(
      When(like_users=user, then=True),
      default=False,
      output_field=BooleanField()
    )
  ).order_by("-update_at", "title")
  context = {
    "username": username,
    "books": books,
  }
  return render(request, "book_app/index.html", context)

def create(request):
  if request.method == "POST":
    user = User.objects.get(id=request.session["user_id"])
    res = Book.objects.create_validate(request.POST, user)
    if res["is_valid"]:
      return redirect(reverse("book:index"))
    errors = res["result"]
    for error in errors.values():
      messages.error(request, error)
  return redirect(reverse("book:index"))

def detail(request, book_id):
  book = Book.objects.get(id=book_id)
  user = User.objects.get(id=request.session["user_id"])
  like_users = list(book.like_users.all())
  context = {
    "user": user,
    "book": book,
    "like_users": like_users
  }
  return render(request, "book_app/detail.html", context)

def update(request, book_id):
  if request.method == "POST":
    res = Book.objects.update_validate(request.POST, book_id)
    if not res["is_valid"]:
      errors = res["result"]
      for error in errors.values():
        messages.error(request, error)
  return redirect(reverse("book:detail", kwargs={"book_id":book_id}))

def add_favorite(request, book_id):
  user = User.objects.get(id=request.session["user_id"])
  user.favorite_books.add(book_id)
  return redirect(reverse("book:detail", kwargs={"book_id":book_id}))

def un_favorite(request, book_id):
  user = User.objects.get(id=request.session["user_id"])
  user.favorite_books.remove(book_id)
  return redirect(reverse("book:detail", kwargs={"book_id":book_id}))

def all_favorite(request):
  user_id = request.session["user_id"]
  books = Book.objects.filter(like_users=User.objects.get(id=user_id))
  user = User.objects.get(id=user_id)
  context = {
    "books": books,
    "user": user
  }
  return render(request, "book_app/allfavorite.html", context)

def delete(request, book_id):
  if request.method == "POST":
    Book.objects.get(id=book_id).delete()
  return redirect(reverse("book:index"))

def logout(request):
  request.session.clear()
  return redirect(reverse("user:index"))




