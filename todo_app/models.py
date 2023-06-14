# todo_list/todo_app/models.p


import datetime

from django.db import models


class ToDoItem(models.Model):

    STATUS_CHOICES = [

        ('Pending','PENDING',),
        ('Completed','COMPLETED'),
        ('In Progress','IN_PROGRESS'),
    ]
    
    title = models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True, blank=True)
    # created_date = models.DateField(default=datetime.date.today)
    # due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    

    def __str__(self):
        return self.title

