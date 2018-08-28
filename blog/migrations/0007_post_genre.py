# Generated by Django 2.0.5 on 2018-08-23 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='genre',
            field=models.CharField(choices=[('barking_news', 'Barking News'), ('sports', 'Sports'), ('paw-litics', 'Paw-litics'), ('weather', 'Weather'), ('re-tail', 'Ret-tail')], default='barking_news', max_length=12),
        ),
    ]
