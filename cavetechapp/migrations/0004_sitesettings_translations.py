# Generated migration for SiteSettings translation fields

from django.db import migrations, models
import django.db.models.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('cavetechapp', '0003_sitesettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='about_title_translations',
            field=django.db.models.fields.json.JSONField(blank=True, default=dict, help_text="Translations: {'nb': '...', 'en': '...', 'zh-hans': '...'}"),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='about_content_translations',
            field=django.db.models.fields.json.JSONField(blank=True, default=dict, help_text="Translations: {'nb': '...', 'en': '...', 'zh-hans': '...'}"),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='history_translations',
            field=django.db.models.fields.json.JSONField(blank=True, default=dict, help_text="Translations: {'nb': '...', 'en': '...', 'zh-hans': '...'}"),
        ),
    ]
