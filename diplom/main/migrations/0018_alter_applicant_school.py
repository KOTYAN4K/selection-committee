# Generated by Django 5.0.4 on 2024-05-01 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_applicant_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='school',
            field=models.CharField(default='default', max_length=255, verbose_name='Адрес проживания'),
            preserve_default=False,
        ),
    ]