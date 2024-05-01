from django.db import models
import datetime


class School(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Школа"
        verbose_name_plural = "Школы"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Отделение"
        verbose_name_plural = "Отделения"

    def __str__(self):
        return self.name


class Applicant(models.Model):
    photo = models.ImageField(upload_to="applicants_photos/", default="applicants_photos/default.jpg",
                              verbose_name="Фото")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, verbose_name="Отчество")
    gender = models.CharField(max_length=10, verbose_name="Пол", choices=(("male", "Мужской"),
                                                                          ("female", "Женский")),
                              default='male')
    birth_date = models.DateField(verbose_name="Дата рождения")
    email = models.EmailField(verbose_name="Эл.Почта")
    address = models.CharField(max_length=255, verbose_name="Адрес проживания")
    # school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="Школа",
    #                            default=None, blank=True, null=True)
    school = models.CharField(max_length=255, verbose_name="Школа")
    YEAR_CHOICES = [(r, r) for r in range(datetime.date.today().year - 24, datetime.date.today().year + 1)]

    graduation_date = models.IntegerField(choices=YEAR_CHOICES, verbose_name="Дата окончания школы",
                                          default="Дата окончания школы")
    status = models.CharField(max_length=20, verbose_name="Статус заявки",
                              choices=(("watching", "Рассмотрение"), ("answered", "Выдан ответ")),
                              default='watching')
    consent = models.FileField(upload_to="consents/",
                               verbose_name='Согласие на обработку данных', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = "Заявка на регистрацию"
        verbose_name_plural = "Заявки на регистрацию"

    def change_status_to_answered(self):
        self.status = 'answered'
        self.save()

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic} - {self.birth_date}"


class Document(models.Model):
    student = models.OneToOneField('Applicant', on_delete=models.CASCADE, verbose_name="Абитуриент",
                                   related_name='document', blank=True, null=True)
    SNILS = models.CharField(max_length=14, verbose_name="СНИЛС", blank=True, null=True)
    INN = models.CharField(max_length=12, verbose_name="ИНН", blank=True, null=True)
    passport_number = models.CharField(max_length=20, verbose_name="Номер паспорта", blank=True, null=True)
    issued_by = models.CharField(max_length=255, verbose_name="Кем выдан", blank=True, null=True)
    issue_date = models.DateField(verbose_name="Дата выдачи", blank=True, null=True)
    certificate = models.CharField(max_length=255, verbose_name="Свидетельство", blank=True, null=True)
    original_or_copy = models.BooleanField(verbose_name="Оригинал или копия", blank=True, null=True, default=False)
    FIS = models.CharField(max_length=255, verbose_name="ФИС", blank=True, null=True)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        if self.student is None:
            return "NULL"
        return f'{self.student}'


class Parent(models.Model):
    student = models.OneToOneField(Applicant, on_delete=models.CASCADE, verbose_name="Ребёнок", blank=True, null=True)
    mother_full_name = models.CharField(max_length=255, verbose_name="ФИО матери", blank=True, null=True)
    mother_phone = models.CharField(max_length=20, verbose_name="Телефон матери", blank=True, null=True)
    father_full_name = models.CharField(max_length=255, verbose_name="ФИО отца", blank=True, null=True)
    father_phone = models.CharField(max_length=20, verbose_name="Телефон отца", blank=True, null=True)

    class Meta:
        verbose_name = "Родитель"
        verbose_name_plural = "Родители"

    def __str__(self):
        return f"Родители {self.student}"


class InternalExam(models.Model):
    exam_date = models.DateTimeField('Дата экзамена', blank=True)
    exam_result = models.CharField('Результаты экзамена', max_length=255, blank=True)
    student = models.OneToOneField('Applicant', on_delete=models.CASCADE, verbose_name="Студент",
                                   related_name='internal_exam')

    class Meta:
        verbose_name = 'Внутренний экзамен'
        verbose_name_plural = 'Внутренний экзамен'

    def __str__(self):
        return str(self.student)


class Admission(models.Model):
    applicant = models.OneToOneField('Applicant', on_delete=models.CASCADE, verbose_name="Абитуриент",
                                     related_name="admission")
    department = models.ManyToManyField('Department', verbose_name="Отделение",
                                        blank=True, null=True)
    admission_date = models.DateField(verbose_name="Дата поступления", auto_now=True)
    number_of_5 = models.IntegerField(default=0, verbose_name="Количество пятерок", blank=True, null=True)
    number_of_4 = models.IntegerField(default=0, verbose_name="Количество четверок", blank=True, null=True)
    number_of_3 = models.IntegerField(default=0, verbose_name="Количество троек", blank=True, null=True)
    average_score = models.DecimalField(default=0.0, max_digits=5, decimal_places=2,
                                        verbose_name="Средний балл", blank=True, null=True)
    application_status = models.CharField(max_length=50, verbose_name="Статус заявки",
                                          choices=(("watching", "Рассмотрение"), ("accepted", "Принят")),
                                          default='watching')
    out_of_budget = models.BooleanField(default=False, verbose_name="Внебюджет", blank=True, null=True)
    received_receipt = models.BooleanField(default=False, verbose_name="Получил расписку", blank=True, null=True)
    internal_exam_conducted = models.BooleanField(default=False, verbose_name="Внутренний экзамен проведен",
                                                  blank=True, null=True)
    documents_collected = models.BooleanField(default=False, verbose_name="Документы забраны", blank=True, null=True)
    application_in_gov_services = models.BooleanField(default=False, verbose_name="Заявление в гос. услугах",
                                                      blank=True, null=True)
    internal_exam = models.OneToOneField(InternalExam, on_delete=models.CASCADE, verbose_name="Внутренний экзамен",
                                         related_name="admission", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', blank=True, null=True)

    class Meta:
        verbose_name = "Поступление"
        verbose_name_plural = "Поступления"

    def change_status_to_answered(self):
        self.application_status = 'accepted'
        self.save()

    def save(self, *args, **kwargs):
        total_scores = self.number_of_5 * 5 + self.number_of_4 * 4 + self.number_of_3 * 3
        total_subjects = self.number_of_5 + self.number_of_4 + self.number_of_3

        if total_subjects != 0:
            self.average_score = total_scores / total_subjects

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.applicant}'
