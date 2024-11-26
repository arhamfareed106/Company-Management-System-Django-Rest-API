from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_add_employee_performance_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='completion_percentage',
            field=models.IntegerField(default=0),
        ),
    ]
