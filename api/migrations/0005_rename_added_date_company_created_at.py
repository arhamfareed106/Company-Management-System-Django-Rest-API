from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_company_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='added_date',
            new_name='created_at',
        ),
    ]
