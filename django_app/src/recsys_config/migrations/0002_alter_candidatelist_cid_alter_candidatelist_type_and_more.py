# Generated by Django 4.1.5 on 2023-02-06 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recsys_config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatelist',
            name='cid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='candidatelist',
            name='type',
            field=models.CharField(choices=[('engage', 'engage'), ('static', 'static')], default='engage', max_length=16),
        ),
        migrations.AlterField(
            model_name='modeldefinition',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='recsys_config.modelservice'),
        ),
        migrations.AlterField(
            model_name='recommenderversion',
            name='cache_key',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='recommenderversion',
            name='model_selection_timeout_min',
            field=models.IntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='segmentmatch',
            name='user_type',
            field=models.CharField(choices=[('ALL', 'ALL'), ('SSO_ID', 'SSO'), ('EB_ID', 'EB'), ('NO_ID', 'NONE')], default='ALL', max_length=20),
        ),
    ]
