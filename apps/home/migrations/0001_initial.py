# Generated by Django 3.2.16 on 2024-11-12 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('date_joined', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='KPI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('target_value', models.FloatField()),
                ('unit', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achieved_value', models.FloatField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.employee')),
                ('kpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.kpi')),
                ('review_cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.reviewcycle')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('performance_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.performancereview')),
            ],
        ),
    ]
