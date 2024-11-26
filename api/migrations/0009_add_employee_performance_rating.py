from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_add_employee_timestamps'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='performance_rating',
            field=models.CharField(
                choices=[('EXC', 'Excellent'), ('GOOD', 'Good'), ('AVG', 'Average'), ('BELOW', 'Below Average'), ('POOR', 'Poor')],
                default='AVG',
                max_length=5
            ),
        ),
    ]
