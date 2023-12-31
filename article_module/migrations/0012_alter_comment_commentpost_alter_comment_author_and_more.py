# Generated by Django 4.1.7 on 2023-06-20 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article_module', '0011_comment_delete_articlecomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='CommentPost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article_module.article', verbose_name='نظر پست'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='نظر'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='article_module.comment', verbose_name='ریپلای'),
        ),
    ]
