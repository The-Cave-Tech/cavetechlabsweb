# Generated migration for SiteSettings model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cavetechapp', '0002_category_alter_project_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_title', models.CharField(default='About The Cave Tech', max_length=200)),
                ('about_content', models.TextField(blank=True, help_text='Main about us content')),
                ('history', models.TextField(blank=True, help_text='History section content')),
                ('address', models.TextField(blank=True, help_text='Physical address')),
                ('email', models.EmailField(blank=True, max_length=254, help_text='Contact email address')),
                ('instagram', models.URLField(blank=True, help_text='Instagram profile URL')),
                ('phone', models.CharField(blank=True, help_text='Contact phone number', max_length=20)),
                ('image', models.ImageField(blank=True, help_text='Hero image for About Us page', null=True, upload_to='about/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
            },
        ),
    ]
