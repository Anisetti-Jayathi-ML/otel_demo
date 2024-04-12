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
logger = logging.getLogger()






class ProjectList(APIView):


    def get(self,request):
        queryset = ProjectModel.objects.all()
        serializer = ProjectSerializer(queryset,many=True)
        # print(serializer)
        logger.info("get projects list")
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def post(self,request):
        try:
            print(request.data)
            serializer = ProjectSerializer(data=request.data)
            logger.info("created project with given details")
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error occurred while processing POST request: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # data = {'message': 'This is a GET request response from the API'}
        # return JsonResponse(data)
       


class ApplicationDetails(APIView):

    def get(self,request,projid):
        apps = AppModel.objects.filter(project_id = projid)
        serializer = AppSerializer(apps,many=True)
        logger.info("get applications in given project")
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def post(self,request,projid):
        try:
            print(request.data)
            logger.info("create application")
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
        except Exception as e:
            logger.error("Error occurred while processing POST request: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # data = {'message': 'This is a GET request response from the API'}
        # return JsonResponse(data)
       
        



