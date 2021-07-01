from django.urls import path
from .views import ProjectListView, ProjectDetailView, CommentListView, CommentDetailView, ProjectFavoriteView

urlpatterns = [
    path('', ProjectListView.as_view()),
    path('<int:pk>/', ProjectDetailView.as_view()),
    path('<int:pk>/favorite/', ProjectFavoriteView.as_view()),
    path('<int:project_pk>/comments/', CommentListView.as_view()),
    path('<int:_project_pk>/comments/<int:comment_pk>/', CommentDetailView.as_view()),
]
