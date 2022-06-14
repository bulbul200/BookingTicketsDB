# Generated by Django 3.2.12 on 2022-05-25 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220525_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passengers',
            name='schedules',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='schedule', to='core.schedules'),
        ),
    ]
