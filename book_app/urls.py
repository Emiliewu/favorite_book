from django.urls import path
from . import views

app_name = "book"

urlpatterns = [
  path("", views.index, name="index"),
  path("create", views.create, name="create"),
  path("<int:book_id>", views.detail, name="detail"),
  path("<int:book_id>/update", views.update, name="update"),
  path("<int:book_id>/delete", views.delete, name="delete"),
  path("<int:book_id>/un_favorite", views.un_favorite, name="un_favorite"),
  path("<int:book_id>/add_favorite", views.add_favorite, name="add_favorite"),
  path("all_favorite", views.all_favorite, name="all_favorite"),
  path("logout", views.logout, name="logout"),
]