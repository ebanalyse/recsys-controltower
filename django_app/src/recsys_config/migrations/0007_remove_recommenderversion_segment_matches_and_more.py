# Generated by Django 4.1.5 on 2023-02-28 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recsys_config', '0006_remove_segmentmatch_models_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommenderversion',
            name='segment_matches',
        ),
        migrations.AddField(
            model_name='segmentmatch',
            name='recommender_version',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='segment_matches', to='recsys_config.recommenderversion'),
            preserve_default=False,
        ),
    ]
