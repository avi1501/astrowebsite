# Generated by Django 3.2.5 on 2021-08-25 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_auto_20210826_0034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vastu',
            options={'ordering': ['-date_created']},
        ),
    ]
