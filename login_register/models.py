from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
  def reg_validate(self, postData):
    errors = {}
    first_name = postData["first_name"]
    last_name = postData["last_name"]
    password = postData["password"]
    email = postData["email"]
    confirm_pw = postData["confirm_pw"]
    if not first_name or first_name.isspace():
      errors["first_name"] = "Please enter your first name"
    elif len(first_name) < 2:
      errors["first_name"] = "First name should have at least 2 charactors"
    elif not first_name.isalpha():
      errors["first_name"] = "Your name should be all letters"
    if not last_name or last_name.isspace():
      errors["last_name"] = "Please enter your last name"
    elif len(last_name) < 2:
      errors["last_name"] = "Last name should have at least 2 charactors"
    elif not last_name.isalpha():
      errors["last_name"] = "Your name should be all letters"
    if not EMAIL_REGEX.match(email):
      errors["email"] = "Invalid email address"
    elif self.filter(email__iexact=email).exists():
      errors["email"] = "This email has already registered"
    if not password or password.isspace():
      errors["password"] = "please enter your password"
    elif len(password) < 8:
      errors["password"] = "Passward shoud have at least 8 charactors"
    elif password != confirm_pw:
      errors["confirm_pw"] = "Your password does not match"
    
    if errors:
      return {"is_valid": False, "result": errors}
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = self.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
    return {"is_valid": True, "result": user.id}

  def login_validate(self, postData):
    email = postData["email"]
    user = self.filter(email=email)
    if user and bcrypt.checkpw(postData["password"].encode(), user[0].password.encode()):
      return {"is_valid": True, "result": user[0].id}
    return {"is_valid": False, "result": "Username and email do not match!"}

class User(models.Model):
  first_name = models.CharField(max_length=45)
  last_name = models.CharField(max_length=45)
  email = models.CharField(max_length=45)
  password = models.CharField(max_length=255)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

  def __str__(self):
    return f"{self.first_name} {self.last_name}"
