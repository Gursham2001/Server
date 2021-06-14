from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Project, Comment
from .serializers import ProjectSerializer, PopulatedProjectSerializer, CommentSerializer

class ProjectListView(APIView):

    def get(self, _request):
        project = Project.objects.all()
        serialized_project = PopulatedProjectSerializer(project, many=True)
        return Response(serialized_project.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['owner'] = request.user.id
        new_project = ProjectSerializer(data=request.data)
        if new_project.is_valid():
            new_project.save()
            return Response(new_project.data, status=status.HTTP_201_CREATED)
        return Response(new_project.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)    

class ProjectDetailView(APIView):

    def get_project(self, pk):
        try :
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound()

    def get(self, _request, pk):
        try :
            project = Project.objects.get(pk=pk) 
            serialized_project = PopulatedProjectSerializer(project)
            return Response(serialized_project.data,status=status.HTTP_200_OK) 
        except Project.DoesNotExist:
            raise NotFound()

    def delete(self, request, pk):
        project_to_delete = self.get_project(pk=pk)
        if project_to_delete.owner != request.user:
            raise PermissionDenied()
        project_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, project_pk):
        request.data['project'] = project_pk
        request.data['owner'] = request.user.id
        serialized_comment = CommentSerializer(data=request.data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        return Response(serialized_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CommentDetailView(APIView):

    def delete(self, request, _project_pk, comment_pk):
        try:
            comment_to_delete = Comment.objects.get(pk=comment_pk)
            if comment_to_delete.owner != request.user:
                raise PermissionDenied()
            comment_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise NotFound()
