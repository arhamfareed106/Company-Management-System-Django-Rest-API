# Generated by Django 5.1.3 on 2024-11-24 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.CharField(choices=[('Manager', 'manager'), ('Software Developer', 'software developer'), ('Project Leader', 'project leader')], max_length=500),
        ),
    ]
