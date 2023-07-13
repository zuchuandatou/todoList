from django.db import models
from django.contrib.auth.models import User  # user info: email, password, etc

# When add new model/update old model:
  # python3 manage.py make migration
  # python3 manage.py migrate
  
class Task(models.Model):
    # one to many relationship: one user, many items
    # on_delete: what to do if delete the user
      # models.CASCADE: if the user is deleted, the tasks are also delete
      # null=True: could be empty field
      # blank=True: when submit form with blank
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # char length max = 200
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    # time stamp
    create = models.DateTimeField(auto_now_add=True)

    # string representation of the model
    def __str__(self):
        return self.title
    
    # order of the query set when return, complete task at bottom
    class Meta:
        ordering = ['complete']