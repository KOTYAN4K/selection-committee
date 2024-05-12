# Generated by Django 5.0.4 on 2024-05-03 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_remove_internalexam_student_internalexam_student'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='internalexam',
            options={'verbose_name': 'Вступительный экзамен', 'verbose_name_plural': 'Вступительный экзамен'},
        ),
        migrations.RemoveField(
            model_name='internalexam',
            name='exam_result',
        ),
        migrations.AddField(
            model_name='admission',
            name='exam_result',
            field=models.CharField(blank=True, max_length=255, verbose_name='Результаты экзамена'),
        ),
    ]