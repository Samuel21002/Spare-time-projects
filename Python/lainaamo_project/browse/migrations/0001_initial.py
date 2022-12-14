# Generated by Django 4.1.1 on 2022-11-09 10:38

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('release_date', models.DateTimeField()),
                ('description', models.CharField(max_length=400)),
                ('file', models.FileField(blank=True, null=True, upload_to='static', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('cover', models.ImageField(blank=True, null=True, upload_to='static', validators=[django.core.validators.validate_image_file_extension])),
                ('authors', models.ManyToManyField(to='browse.author')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('verbal_review', models.TextField(max_length=400)),
                ('release', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='browse.release')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_date', models.DateTimeField(default=datetime.datetime(2022, 11, 9, 10, 38, 21, 516646, tzinfo=datetime.timezone.utc))),
                ('return_date', models.DateTimeField(default=datetime.datetime(2022, 11, 23, 10, 38, 21, 516957))),
                ('returned', models.BooleanField(default=False)),
                ('release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='browse.release')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='release',
            name='topics',
            field=models.ManyToManyField(blank=True, null=True, to='browse.topic'),
        ),
    ]
