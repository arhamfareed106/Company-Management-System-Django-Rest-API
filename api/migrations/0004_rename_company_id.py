from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20241126_1920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='company_id',
            new_name='id',
        ),
    ]
