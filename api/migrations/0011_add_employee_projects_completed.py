from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_add_project_completion_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='projects_completed',
            field=models.IntegerField(default=0),
        ),
    ]
