from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20241126_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='established_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='company',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='type',
            field=models.CharField(choices=[('CORP', 'Corporation'), ('LLC', 'Limited Liability Company'), ('PART', 'Partnership'), ('SOLE', 'Sole Proprietorship')], default='CORP', max_length=4),
        ),
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.URLField(blank=True),
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name'], 'verbose_name_plural': 'Companies'},
        ),
    ]
