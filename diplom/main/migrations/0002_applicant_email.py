# Generated by Django 5.0.2 on 2024-04-01 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='email',
            field=models.EmailField(default='ex@mail.ru', max_length=254, verbose_name='Эл.Почта'),
            preserve_default=False,
        ),
    ]
