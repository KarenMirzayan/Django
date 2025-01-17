from rest_framework.viewsets import ModelViewSet 

from .models import User, Project, Category, Priority, Task 

from .serializers import UserSerializer, ProjectSerializer, CategorySerializer, PrioritySerializer, TaskSerializer 

from rest_framework.filters import SearchFilter 

from django_filters.rest_framework import DjangoFilterBackend 

import logging 

logger = logging.getLogger(__name__) 
 

class UserViewSet(ModelViewSet): 

    queryset = User.objects.all() 

    serializer_class = UserSerializer 

 

class ProjectViewSet(ModelViewSet): 

    queryset = Project.objects.all() 

    serializer_class = ProjectSerializer 

 

class CategoryViewSet(ModelViewSet): 

    queryset = Category.objects.all() 

    serializer_class = CategorySerializer 

 

class PriorityViewSet(ModelViewSet): 

    queryset = Priority.objects.all() 

    serializer_class = PrioritySerializer 

 

class TaskViewSet(ModelViewSet): 

    queryset = Task.objects.all() 

    serializer_class = TaskSerializer 
    
    # filter_backends = [DjangoFilterBackend, SearchFilter] 

    # filterset_fields = ['project', 'priority', 'category'] 

    # search_fields = ['title', 'description'] 
    
    def perform_create(self, serializer): 

        logger.info("Creating a new task") 

        serializer.save() 
