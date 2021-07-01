from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from project_expo.serializers import ProjectSerializer
from project_expo.serializers import CommentSerializer
# from jwt_auth.serializers import UserSerializer

User = get_user_model()

class PopulatedUserSerializer(ModelSerializer):
    favorites = ProjectSerializer(many=True)
    comments = CommentSerializer(many=True)
    created_project = ProjectSerializer(many=True)


    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'profile_image',
            'email',
            'favorites',
            'comments',
            'created_project',
            'gacohort',
            'linkedin',
            'github',
            'twitter',
            'personalsite',
            'instagram',
            'job_title'
        )
