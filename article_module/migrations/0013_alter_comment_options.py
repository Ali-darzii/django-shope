# Generated by Django 4.1.7 on 2023-06-21 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0012_alter_comment_commentpost_alter_comment_author_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date_posted'], 'verbose_name': 'نظرات', 'verbose_name_plural': 'نظرات'},
        ),
    ]
