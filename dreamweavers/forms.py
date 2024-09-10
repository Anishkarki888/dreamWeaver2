from django import forms
from service.models import CallBackRequest
from service.models import Application
from service.models import Document
from service.models import Feedback


class userForms(forms.Form):
    name=forms.CharField()
    reason=forms.CharField()
    email=forms.CharField()
    phone=forms.CharField()


class CallBackRequestForm(forms.ModelForm):
    class Meta:
        model = CallBackRequest
        fields = ['name', 'phone', 'subject']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'country', 'email', 'phone', 'application_type']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['citizenship_passport', 'transcript', 'ielts_score', 'sop', 'bank_balance']

# class FeedbackForm(forms.ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ['feedback']  # Add feedback field to your Document model if it doesn't exist yet

# #     feedback = forms.CharField(widget=forms.Textarea, required=False)
        
# class FeedbackForm(forms.Form):
#     document_id = forms.IntegerField(widget=forms.HiddenInput())
#     feedback_text = forms.CharField(widget=forms.Textarea)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text'] 
    
    document_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)


class UniversityRecommendationForm(forms.Form):
    city = forms.CharField(label='City', max_length=100)
    country = forms.CharField(label='Country', max_length=100)
    cost = forms.IntegerField(label='Cost')
    subjects = forms.CharField(label='Preferred Subjects')
    ielts = forms.FloatField(label='IELTS Score')
