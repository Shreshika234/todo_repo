# todo_list/todo_app/models.p
from django.db import models

class ToDoItem(models.Model):

    STATUS_CHOICES = [

        ('Pending','PENDING',),
        ('Completed','COMPLETED'),
        ('In Progress','IN_PROGRESS'),
    ]
    username = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    # file = models.FileField(upload_to="taskfiles/",max_length=150,null=True,default=None)

    def __str__(self):
        return self.title

