# Generated by Django 3.2.4 on 2021-06-18 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0002_user_created_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='GAcohort',
            field=models.TextField(blank=True, max_length=50),
        ),
    ]