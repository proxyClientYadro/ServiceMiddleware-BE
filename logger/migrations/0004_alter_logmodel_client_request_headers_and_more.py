# Generated by Django 4.2.7 on 2023-12-27 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0003_rename_proxy_method_logmodel_client_request_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logmodel',
            name='client_request_headers',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='core_response_headers',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='proxy_request_headers',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='proxy_response_headers',
            field=models.TextField(blank=True, null=True),
        ),
    ]