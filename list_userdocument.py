# management/commands/list_user_documents.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from service.models import Document  # Replace 'your_app' with the name of your Django app

class Command(BaseCommand):
    help = 'List documents for each user'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            documents = Document.objects.filter(user=user)
            self.stdout.write(f'Documents for {user.username}:')
            for doc in documents:
                self.stdout.write(f' - {doc.citizenship_passport}, {doc.transcript}, {doc.ielts_score}, {doc.sop}, {doc.bank_balance}')
