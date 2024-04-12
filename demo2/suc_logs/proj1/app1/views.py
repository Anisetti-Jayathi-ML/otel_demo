from django.shortcuts import render
from rest_framework import generics
from .models import ProjectModel,AppModel
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import ProjectSerializer,AppSerializer
from rest_framework import status
import logging
import os
#logger = logging.getLogger()
# logging.info("get projects list")
#         logging.debug("dsfds")
#         logging.error("dsfds")




class ProjectList(APIView):


    def get(self,request):
        queryset = ProjectModel.objects.all()
        serializer = ProjectSerializer(queryset,many=True)
        # print(serializer)
        logging.info("get projects list")
        logging.debug("debug log")
        logging.error("error log")
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def post(self,request):
        print(request.data)
        serializer = ProjectSerializer(data=request.data)
        logging.info("created project with given details")
        
        if serializer.is_valid():
            serializer.save()
            # logger.info(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetails(APIView):

    def get(self,request,projid):
        apps = AppModel.objects.filter(project_id = projid)
        serializer = AppSerializer(apps,many=True)
        logging.info("get applications in given project")
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def post(self,request,projid):
        print(request.data)
        logging.info("create application")
        new_data = dict(request.data)
        new_data['project_id'] = projid
        if 'application_name' in new_data.keys():
            new_data['application_name'] = new_data['application_name'][0]
        if 'application_type' in new_data.keys():
            new_data['application_type'] = new_data['application_type'][0]
        if 'description' in new_data.keys():
            new_data['description'] = new_data['description'][0]
        print((new_data))
        serializer = AppSerializer(data=new_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # data = {'message': 'This is a GET request response from the API'}
        # return JsonResponse(data)
       
        



