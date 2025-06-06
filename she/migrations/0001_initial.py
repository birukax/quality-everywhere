# Generated by Django 5.1.4 on 2025-03-13 12:06

import datetime
import django.db.models.deletion
import main.validators
import she.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IncidentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IssueType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('no', models.CharField(max_length=20, unique=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Terminated', 'Terminated')], default='Active', max_length=20)),
                ('employment_date', models.DateField(blank=True, null=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='employees', to='she.department')),
            ],
            options={
                'ordering': ['name', 'no'],
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CREATED', 'CREATED'), ('CANCELLED', 'CANCELLED'), ('PENDING', 'PENDING'), ('INCOMPLETE', 'INCOMPLETE'), ('COMPLETED', 'COMPLETED')], default='CREATED', max_length=20)),
                ('type', models.CharField(choices=[('PRODUCTION', 'PRODUCTION'), ('SAFETY', 'SAFETY')], default='SAFETY', max_length=20)),
                ('observation', models.TextField(max_length=200)),
                ('suggestion', models.TextField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, help_text='Upload Image', null=True, upload_to=she.models.issue_image_upload_path, validators=[main.validators.validate_image])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='issues', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='issues', to='she.department')),
                ('issue_type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='issues', to='she.issuetype')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='issues', to='she.location')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('time', models.TimeField(default=datetime.datetime.now)),
                ('referred_to_hospital', models.BooleanField(default=False)),
                ('cause', models.TextField(max_length=200)),
                ('body_part_injured', models.CharField(max_length=75)),
                ('nature_of_injury', models.CharField(max_length=75)),
                ('pre_incident_activity', models.TextField(max_length=100)),
                ('tools_used_before_incident', models.TextField(max_length=100)),
                ('recommendation', models.TextField(max_length=100)),
                ('action_taken', models.TextField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='incidents', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='incidents', to='she.employee')),
                ('witness_list', models.ManyToManyField(blank=True, related_name='witnessed_incidents', to='she.employee')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='incidents', to='she.incidenttype')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='incidents', to='she.location')),
            ],
            options={
                'ordering': ['-date', 'time'],
            },
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('CREATED', 'CREATED'), ('CANCELLED', 'CANCELLED'), ('PENDING', 'PENDING'), ('INCOMPLETE', 'INCOMPLETE'), ('COMPLETED', 'COMPLETED')], max_length=20)),
                ('text', models.TextField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='remarks', to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='remarks', to='she.issue')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
