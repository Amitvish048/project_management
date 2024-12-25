from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer

class ClientListCreateView(generics.ListCreateAPIView):
    """
    Handles listing all clients and creating a new client.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a client.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'


class ProjectCreateView(generics.CreateAPIView):
    """
    Handles creating a new project and assigning it to a client.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Retrieve client ID from the request data
        client_id = request.data.get('client_id')
        if not client_id:
            return Response({"error": "client_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that the client exists
        client = get_object_or_404(Client, pk=client_id)

        # Validate user assignments
        users = request.data.get('users', [])
        if not isinstance(users, list):
            return Response({"error": "users must be a list of user IDs"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and save the project
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save(client=client, created_by=request.user)

        # Assign users to the project
        project.users.set(users)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectListView(generics.ListAPIView):
    """
    Handles listing all projects assigned to the logged-in user.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(users=user)


class ProjectDeleteView(generics.DestroyAPIView):
    """
    Handles deleting a project.
    """
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
