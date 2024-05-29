# resources.py
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import ApplicantAdmissionView, Applicant, Admission, Document, Parent


class ApplicantAdmissionViewResource(resources.ModelResource):
    applicant_full_name = fields.Field(attribute='applicant', column_name='ФИО абитуриента',
                                       widget=ForeignKeyWidget(Applicant, 'last_name'))
    admission_status = fields.Field(attribute='admission', column_name='Статус заявки',
                                    widget=ForeignKeyWidget(Admission, 'application_status'))
    document_snils = fields.Field(attribute='document', column_name='СНИЛС', widget=ForeignKeyWidget(Document, 'SNILS'))
    parent_names = fields.Field(attribute='parent', column_name='Родители',
                                widget=ForeignKeyWidget(Parent, 'mother_full_name'))

    class Meta:
        model = ApplicantAdmissionView
        fields = (
            'applicant_full_name', 'admission_status', 'document_snils', 'parent_names',
            'applicant__last_name', 'applicant__first_name', 'applicant__patronymic',
            'applicant__gender', 'applicant__birth_date', 'applicant__email', 'applicant__phone',
            'applicant__address', 'applicant__school', 'applicant__graduation_date', 'applicant__education',
            'applicant__status', 'admission__department', 'admission__admission_date',
            'admission__number_of_5', 'admission__number_of_4', 'admission__number_of_3',
            'admission__average_score', 'admission__internal_exam', 'admission__application_status',
            'admission__original_or_copy', 'admission__out_of_budget', 'admission__received_receipt',
            'admission__internal_exam_conducted', 'admission__documents_collected',
            'admission__application_in_gov_services', 'document__SNILS', 'document__INN',
            'document__passport_number', 'document__issued_by', 'document__issue_date',
            'document__certificate', 'document__FIS', 'parent__mother_full_name', 'parent__mother_phone',
            'parent__father_full_name', 'parent__father_phone'
        )
        export_order = fields

    def dehydrate_applicant_full_name(self, obj):
        return f"{obj.applicant.last_name} {obj.applicant.first_name} {obj.applicant.patronymic}"

    def dehydrate_admission_status(self, obj):
        return obj.admission.application_status

    def dehydrate_document_snils(self, obj):
        return obj.document.SNILS

    def dehydrate_parent_names(self, obj):
        return f"{obj.parent.mother_full_name}, {obj.parent.father_full_name}"
