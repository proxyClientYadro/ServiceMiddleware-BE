# Generated by Django 4.2.7 on 2024-01-11 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0004_alter_logmodel_client_request_headers_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logmodel',
            options={'ordering': ('id', 'proxy_method'), 'verbose_name': 'Log', 'verbose_name_plural': 'Logs'},
        ),
        migrations.RenameField(
            model_name='logmodel',
            old_name='client_request_method',
            new_name='core_method',
        ),
        migrations.RenameField(
            model_name='logmodel',
            old_name='client_request_body',
            new_name='core_request_body',
        ),
        migrations.RenameField(
            model_name='logmodel',
            old_name='client_request_headers',
            new_name='core_request_headers',
        ),
        migrations.RenameField(
            model_name='logmodel',
            old_name='client_request_url',
            new_name='core_url',
        ),
        migrations.RenameField(
            model_name='logmodel',
            old_name='proxy_request_method',
            new_name='proxy_method',
        ),
        migrations.RenameField(
            model_name='logmodel',
            old_name='proxy_request_url',
            new_name='proxy_url',
        ),
    ]
