from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_added_date_company_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='employee_id',
            new_name='id',
        ),
    ]
