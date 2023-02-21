# Generated by Django 4.1.5 on 2023-02-19 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LOGIN_TRY',
            fields=[
                ('ip', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('count', models.DecimalField(decimal_places=0, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='PUSH_SCHEDULE_TABLE',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=20)),
                ('alias', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('message', models.CharField(max_length=255)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField()),
                ('repeat', models.BooleanField()),
                ('ad', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='QUESTION_TABLE',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('question', models.CharField(max_length=255)),
                ('answer', models.CharField(max_length=255)),
                ('create_datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TARGET_TABLE',
            fields=[
                ('token', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=20)),
                ('uuid', models.CharField(max_length=20)),
                ('is_push_allow', models.BooleanField()),
                ('push_allow_datetime', models.DateTimeField(blank=True, null=True)),
                ('is_ad_allow', models.BooleanField()),
                ('ad_allow_datetime', models.DateTimeField(blank=True, null=True)),
                ('last_active_datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='USER_ACCESS_LOG',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=10)),
                ('ip', models.CharField(max_length=16)),
                ('create_datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='USER_TABLE',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('app_icon', models.ImageField(upload_to='icon')),
                ('app_name', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=64)),
                ('tel', models.CharField(max_length=16)),
                ('url', models.CharField(max_length=255)),
                ('kakao_admin_key', models.CharField(max_length=255)),
                ('create_datetime', models.DateTimeField()),
                ('request_update', models.BooleanField()),
                ('google_form_url', models.CharField(max_length=255)),
                ('download_count', models.DecimalField(decimal_places=0, max_digits=10)),
                ('user_count', models.DecimalField(decimal_places=0, max_digits=10)),
                ('visit_today_count', models.DecimalField(decimal_places=0, max_digits=10)),
                ('total_visit_count', models.DecimalField(decimal_places=0, max_digits=20)),
                ('is_splash', models.BooleanField()),
                ('splash_background', models.ImageField(upload_to='splash_background')),
                ('splash_logo', models.ImageField(upload_to='splash_logo')),
                ('splash_min_time', models.DecimalField(decimal_places=0, max_digits=1)),
                ('layout_type', models.DecimalField(decimal_places=0, max_digits=1)),
                ('theme', models.DecimalField(decimal_places=0, max_digits=1)),
            ],
        ),
        migrations.CreateModel(
            name='USER_UPDATE_LOG',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=10)),
                ('update_log', models.CharField(max_length=255)),
                ('create_datetime', models.DateTimeField()),
            ],
        ),
    ]
