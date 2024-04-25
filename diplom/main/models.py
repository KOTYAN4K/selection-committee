from django.db import models


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
                              verbose_name="Фото", blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, verbose_name="Отчество")
    gender = models.CharField(max_length=10, verbose_name="Пол", choices=(("male", "Мужской"),
                                                                          ("female", "Женский")),
                              default='male')
    birth_date = models.DateField(verbose_name="Дата рождения")
    email = models.EmailField(verbose_name="Эл.Почта")
    address = models.CharField(max_length=255, verbose_name="Адрес проживания")
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="Школа", blank=True, null=True)
    graduation_date = models.DateField(verbose_name="Дата окончания школы", auto_now=False, auto_now_add=False,
                                       blank=True, null=True)
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
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name="Отделение")
    admission_date = models.DateField(verbose_name="Дата поступления")
    out_of_budget = models.BooleanField(default=False, verbose_name="Внебюджет")
    number_of_5 = models.IntegerField(default=0, verbose_name="Количество пятерок")
    number_of_4 = models.IntegerField(default=0, verbose_name="Количество четверок")
    number_of_3 = models.IntegerField(default=0, verbose_name="Количество троек")
    average_score = models.FloatField(default=0.0, verbose_name="Средний балл")
    received_receipt = models.BooleanField(default=False, verbose_name="Получил расписку")
    application_status = models.CharField(max_length=50, verbose_name="Статус заявки")
    internal_exam_conducted = models.BooleanField(default=False, verbose_name="Внутренний экзамен проведен")
    application_number = models.IntegerField(verbose_name="Номер заявления")
    documents_collected = models.BooleanField(default=False, verbose_name="Документы забраны")
    application_in_gov_services = models.BooleanField(default=False, verbose_name="Заявление в гос. услугах")
    internal_exam = models.OneToOneField(InternalExam, on_delete=models.CASCADE, verbose_name="Внутренний экзамен",
                                         related_name="admission", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = "Поступление"
        verbose_name_plural = "Поступления"

    def __str__(self):
        return self.applicant
