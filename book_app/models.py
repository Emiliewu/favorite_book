from django.db import models
from login_register.models import User
from django.utils import timezone

class BookManager(models.Manager):
  def create_validate(self, postData, user):
    errors = {}
    title = postData["title"].strip()
    desc = postData["desc"].strip()
    if not title or title.isspace():
      errors["title"] = "The book title cannot be empty"
    elif self.filter(title__iexact=title).exists():
      errors["title"] = "This book title has already uploaded"
    if not desc or desc.isspace():
      errors["desc"] = "The description cannot be empty"
    elif len(desc) <= 5:
      errors["desc"] = "The description should be longer than 5 charactors"
    if errors:
      return {"is_valid": False, "result": errors}
    book = self.create(title=title, desc=desc, upload_user=user)
    user.favorite_books.add(book)
    return {"is_valid": True}    

  def update_validate(self, postData, book_id):
    errors = {}
    title = postData["title"].strip()
    desc = postData["desc"].strip()
    if not title or title.isspace():
      errors["title"] = "The book title cannot be empty"
    elif self.exclude(id=book_id).filter(title__iexact=title).exists():
      errors["title"] = "That book title has already uploaded"
    if not desc or desc.isspace():
      errors["desc"] = "The description cannot be empty"
    elif len(desc) <= 5:
      errors["desc"] = "The description should be longer than 5 charactors"
    if self.filter(title=title, desc=desc).exists():
      errors["unchanged"] = "Nothing changed!"
    if errors:
      return {"is_valid": False, "result": errors}
    self.filter(id=book_id).update(title=title, desc=desc, update_at=timezone.now())
    return {"is_valid": True}  

class Book(models.Model):
  title = models.CharField(max_length=255)
  desc = models.TextField()
  upload_user = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
  like_users = models.ManyToManyField(User, related_name="favorite_books")
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  objects = BookManager()
  
  def __str__(self):
    return self.title

