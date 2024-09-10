from django.contrib import admin
from service.models import Service
from .models import Document

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_icon', 'service_title', 'service_des')

admin.site.register(Service, ServiceAdmin)

# @admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at', 'citizenship_passport', 'transcript', 'ielts_score', 'sop', 'bank_balance')

admin.site.register(Document, DocumentAdmin)