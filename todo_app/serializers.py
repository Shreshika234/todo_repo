import datetime
from rest_framework import serializers
from .models import ToDoItem


class ToDoItemSerializer(serializers.ModelSerializer):
    STATUS_CHOICES = [

        ('Pending','PENDING',),
        ('Completed','COMPLETED'),
        ('In Progress','IN_PROGRESS'),
    ]
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)
    # created_date = serializers.DateField(default=datetime.date.today)
    # due_date = serializers.DateField()
    status = serializers.CharField(max_length=20)#, choices=STATUS_CHOICES, default='PENDING')


    class Meta:
        model = ToDoItem
        fields = "__all__"