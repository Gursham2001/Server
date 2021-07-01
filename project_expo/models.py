from django.db import models

class ProjectType(models.Model):
    type = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.type}'

class Project(models.Model):
    project_name = models.CharField(max_length=25)
    url = models.CharField(max_length=300)
    project_type = models.ManyToManyField(
        ProjectType,
        related_name='project',
        blank=True
    )
    favorited_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='favorites',
        blank= True
        ### ? no delete functionalities for many to many relationships
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='created_projects',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.project_name}'

class Comment(models.Model):
    content = models.TextField(max_length=250)
    project =  models.ForeignKey(
        Project,
        related_name='comments',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='comments',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'comment {self.id} on {self.project}'
