from django.db import models


class School(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    class Meta:
        verbose_name = "Школа"
        verbose_name_plural = "Школы"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Отделение"
        verbose_name_plural = "Отделения"

    def __str__(self):
        return self.name


class Document(models.Model):
    student = models.OneToOneField('Applicant', on_delete=models.CASCADE, verbose_name="Абитуриент",
                                   related_name='document')
    SNILS = models.CharField(max_length=14, verbose_name="СНИЛС")
    INN = models.CharField(max_length=12, verbose_name="ИНН")
    passport_number = models.CharField(max_length=20, verbose_name="Номер паспорта")
    issued_by = models.CharField(max_length=255, verbose_name="Кем выдан")
    issue_date = models.DateField(verbose_name="Дата выдачи")
    certificate = models.CharField(max_length=255, verbose_name="Свидетельство")
    original_or_copy = models.CharField(max_length=20, verbose_name="Оригинал или копия")
    FIS = models.CharField(max_length=255, verbose_name="ФИС")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.certificate


class Parent(models.Model):
    mother_full_name = models.CharField(max_length=255, verbose_name="ФИО матери")
    mother_phone = models.CharField(max_length=20, verbose_name="Телефон матери")
    father_full_name = models.CharField(max_length=255, verbose_name="ФИО отца")
    father_phone = models.CharField(max_length=20, verbose_name="Телефон отца")

    class Meta:
        verbose_name = "Родитель"
        verbose_name_plural = "Родители"

    def __str__(self):
        return f"{self.mother_full_name} и {self.father_full_name}"


class Applicant(models.Model):
    photo = models.ImageField(upload_to="applicants_photos/", verbose_name="Фото", blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, verbose_name="Отчество")
    gender = models.CharField(max_length=10, verbose_name="Пол", choices=(("male", "Мужской"),
                                                                          ("female", "Женский")),
                              default='female')
    birth_date = models.DateField(verbose_name="Дата рождения")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Эл.Почта")
    address = models.CharField(max_length=255, verbose_name="Адрес проживания")
    parents = models.ForeignKey(Parent, on_delete=models.CASCADE, verbose_name="Родители", blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="Школа", blank=True, null=True)
    graduation_date = models.DateField(verbose_name="Дата окончания школы", blank=True, null=True)
    time_created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, verbose_name="Статус заявки",
                              choices=(("watching", "Рассмотрение"), ("answered", "Выдан ответ")),
                              default='watching')

    class Meta:
        verbose_name = "Абитуриент"
        verbose_name_plural = "Абитуриенты"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic} - {self.birth_date}"


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

    class Meta:
        verbose_name = "Поступление"
        verbose_name_plural = "Поступления"

    def __str__(self):
        return self.applicant
