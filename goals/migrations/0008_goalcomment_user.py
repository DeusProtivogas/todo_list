# Generated by Django 4.0.1 on 2022-08-26 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0007_alter_goalcategory_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalcomment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='goal_comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
