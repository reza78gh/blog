# Generated by Django 3.1.4 on 2021-02-08 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0004_auto_20210208_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weblog.category', verbose_name='عنوان'),
        ),
    ]