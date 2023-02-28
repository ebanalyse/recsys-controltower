# Generated by Django 4.1.5 on 2023-02-28 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recsys_config', '0005_alter_modeldefinition_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='segmentmatch',
            name='models',
        ),
        migrations.AddField(
            model_name='modeldefinition',
            name='segment_match',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='model_definitions', to='recsys_config.segmentmatch'),
            preserve_default=False,
        ),
    ]