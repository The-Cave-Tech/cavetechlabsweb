# Generated migration file
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('title', models.CharField(blank=True, help_text='e.g., Founder, Lead Instructor', max_length=200)),
                ('bio', models.TextField(blank=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('image', models.ImageField(blank=True, null=True, upload_to='people/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'People',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('3d_printing', '3D Printing'), ('woodworking', 'Woodworking'), ('metalworking', 'Metalworking'), ('electronics', 'Electronics'), ('software', 'Software'), ('art', 'Art & Design'), ('robotics', 'Robotics'), ('other', 'Other')], max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='projects/')),
                ('featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='cavetechapp.person')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
