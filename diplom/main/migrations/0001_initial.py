# Generated by Django 5.0.2 on 2024-02-22 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='applicants_photos/', verbose_name='Фото')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=100, verbose_name='Отчество')),
                ('gender', models.CharField(max_length=10, verbose_name='Пол')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес проживания')),
                ('graduation_date', models.DateField(blank=True, null=True, verbose_name='Дата окончания школы')),
            ],
            options={
                'verbose_name': 'Абитуриент',
                'verbose_name_plural': 'Абитуриенты',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Отделение',
                'verbose_name_plural': 'Отделения',
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mother_full_name', models.CharField(max_length=255, verbose_name='ФИО матери')),
                ('mother_phone', models.CharField(max_length=20, verbose_name='Телефон матери')),
                ('father_full_name', models.CharField(max_length=255, verbose_name='ФИО отца')),
                ('father_phone', models.CharField(max_length=20, verbose_name='Телефон отца')),
            ],
            options={
                'verbose_name': 'Родитель',
                'verbose_name_plural': 'Родители',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Школа',
                'verbose_name_plural': 'Школы',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SNILS', models.CharField(max_length=14, verbose_name='СНИЛС')),
                ('INN', models.CharField(max_length=12, verbose_name='ИНН')),
                ('passport_number', models.CharField(max_length=20, verbose_name='Номер паспорта')),
                ('issued_by', models.CharField(max_length=255, verbose_name='Кем выдан')),
                ('issue_date', models.DateField(verbose_name='Дата выдачи')),
                ('certificate', models.CharField(max_length=255, verbose_name='Свидетельство')),
                ('original_or_copy', models.CharField(max_length=20, verbose_name='Оригинал или копия')),
                ('FIS', models.CharField(max_length=255, verbose_name='ФИС')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='document', to='main.applicant', verbose_name='Абитуриент')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
        migrations.CreateModel(
            name='InternalExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_date', models.DateTimeField(blank=True, verbose_name='Дата экзамена')),
                ('exam_result', models.CharField(blank=True, max_length=255, verbose_name='Результаты экзамена')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='internal_exam', to='main.applicant', verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Внутренний экзамен',
                'verbose_name_plural': 'Внутренний экзамен',
            },
        ),
        migrations.CreateModel(
            name='Admission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission_date', models.DateField(verbose_name='Дата поступления')),
                ('out_of_budget', models.BooleanField(default=False, verbose_name='Внебюджет')),
                ('number_of_5', models.IntegerField(default=0, verbose_name='Количество пятерок')),
                ('number_of_4', models.IntegerField(default=0, verbose_name='Количество четверок')),
                ('number_of_3', models.IntegerField(default=0, verbose_name='Количество троек')),
                ('average_score', models.FloatField(default=0.0, verbose_name='Средний балл')),
                ('received_receipt', models.BooleanField(default=False, verbose_name='Получил расписку')),
                ('application_status', models.CharField(max_length=50, verbose_name='Статус заявки')),
                ('internal_exam_conducted', models.BooleanField(default=False, verbose_name='Внутренний экзамен проведен')),
                ('application_number', models.IntegerField(verbose_name='Номер заявления')),
                ('documents_collected', models.BooleanField(default=False, verbose_name='Документы забраны')),
                ('application_in_gov_services', models.BooleanField(default=False, verbose_name='Заявление в гос. услугах')),
                ('applicant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admission', to='main.applicant', verbose_name='Абитуриент')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.department', verbose_name='Отделение')),
                ('internal_exam', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admission', to='main.internalexam', verbose_name='Внутренний экзамен')),
            ],
            options={
                'verbose_name': 'Поступление',
                'verbose_name_plural': 'Поступления',
            },
        ),
        migrations.AddField(
            model_name='applicant',
            name='parents',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.parent', verbose_name='Родители'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.school', verbose_name='Школа'),
        ),
    ]
