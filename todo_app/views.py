from django.shortcuts import render
# from requests import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from todo_app.models import ToDoItem
from todo_app.serializers import ToDoItemSerializer

# Create your views here.
class Details(APIView):


    def get(self,request,*args,**kwargs):
        result = ToDoItem.objects.all()
        serializers = ToDoItemSerializer(result,many=True)
        data_list = serializers.data
        return Response(data_list,status=status.HTTP_200_OK)
  

    def post(self,request):
        serializer = ToDoItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"status":"error","data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

    # def patch(self, request):
    #     title = request.data.get('title')
    #     result = ToDoItem.objects.get(title=title)
    #     serializer = ToDoItemSerializer(result,data=request.data,partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"data":serializer.data},status=status.HTTP_200_OK)
    #     else:
    #         return Response({"status":"error","data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from django.conf import settings

class DataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split()[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']   
            data = {"WOW":"WOW"}
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=401)