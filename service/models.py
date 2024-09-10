from django.db import models
from django.contrib.auth.models import User
class Service(models.Model):
    service_icon=models.CharField(max_length=50)
    service_title=models.CharField(max_length=50)
    service_des=models.TextField()


class CallBackRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} - {self.phone}'
    

# class Application(models.Model):
class Application(models.Model):
    APPLICATION_TYPES = [
        ('Education', 'Education'),
        ('Employment', 'Employment'),
    ]

    name = models.CharField(max_length=255)
    country = models.TextField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPES)

    def __str__(self):
        return f'{self.name} - {self.application_type}'
    

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    citizenship_passport = models.FileField(upload_to='documents/')
    transcript = models.FileField(upload_to='documents/')
    ielts_score = models.FileField(upload_to='documents/')
    sop = models.FileField(upload_to='documents/')
    bank_balance = models.FileField(upload_to='documents/')
    feedback = models.TextField(blank=True, null=True) 
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}'s Application Documents"

class Feedback(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE,related_name='feedbacks')
    # admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks_given')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks_received')
    feedback_text = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
        # return f"Feedback from {self.admin.username} for {self.user.username}"
