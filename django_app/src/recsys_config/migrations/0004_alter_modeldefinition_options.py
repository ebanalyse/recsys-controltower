# Generated by Django 4.1.5 on 2023-02-28 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recsys_config', '0003_modeldefinition_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modeldefinition',
            options={'ordering': ['-created']},
        ),
    ]
