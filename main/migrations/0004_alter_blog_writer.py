# Generated by Django 4.1 on 2023-04-11 21:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0003_alter_blog_writer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="writer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
