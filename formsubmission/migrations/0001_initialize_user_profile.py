# Generated by Django 4.2.5 on 2023-10-01 16:15

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('date_of_birth', models.DateField()),
                ('education_background', models.TextField()),
                ('preferred_contact', models.CharField(choices=[('email', 'Email'), ('phone', 'Phone'), ('none', 'None')], max_length=10)),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is Deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted At')),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
    ]
