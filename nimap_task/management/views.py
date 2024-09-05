from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from django.contrib.auth.models import User

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        client = Client.objects.get(pk=self.kwargs['client_pk'])
        serializer.save(client=client, created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def my_projects(self, request):
        user = request.user
        projects = user.projects.all()
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

def root_view(request):
    return HttpResponse("Welcome to the API. Use /api/ to access the endpoints.")
