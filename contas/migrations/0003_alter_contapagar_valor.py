# Generated by Django 4.2.3 on 2023-07-12 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0002_alter_contapagar_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagar',
            name='valor',
            field=models.FloatField(),
        ),
    ]