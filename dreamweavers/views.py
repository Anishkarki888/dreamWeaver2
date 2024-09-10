from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import userForms
from service.models import Service
from service.models import CallBackRequest
# from service.models import ApplicationForm
from dreamweavers.forms import ApplicationForm
from dreamweavers.forms import DocumentForm
from service.models import Document
from django.contrib.auth.decorators import login_required, user_passes_test
from service.models import Feedback
from .forms import FeedbackForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
import requests

def homepage(request):
    servicesData= Service.objects.all()
    for a in servicesData:
        print(a.service_icon)
    
    data={
        'serviceData':servicesData
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')

        CallBackRequest.objects.create(name=name, phone=phone, subject=subject)

        return redirect('home')
    
    return render(request,"index.html")


# def education(request):
#     return render(request,"education.html")


def employment(request):
    return render(request,"employment.html")


def apply(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            application = form.save()

            # Send an email with the form data
            subject = f'New {application.application_type} Apply from {application.name}'
            message = (
                f"Full Name: {application.name}\n"
                f"Email: {application.email}\n"
                f"Phone: {application.phone}\n"
                f"Application Type: {application.application_type}\n"

            )
            recipient_email = 'thisiselonmusk242@gmail.com'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('apply')  # Redirect back to the apply page
        else:
            messages.error(request, 'There was an error with your submission. Please correct the errors below.')

    else:
        form = ApplicationForm()

    return render(request, 'apply.html', {'form': form})

def course(request):
    return render(request,"course.html")

def signup(request):
    context = {}

    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if User.objects.filter(username=uname).exists():
            context['error'] = "Username already exists"
        
        elif pass1 != pass2:
            return HttpResponse("Passwords do not match")
        
        else:
        
            myuser = User.objects.create_user(uname, email, pass1)
            myuser.save()
            return redirect('login')
    
    return render(request, 'signup.html')
        
   

def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        # pass1=request.POST.get('password')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('updates')

            # if username == 'admin' and password == 'admin':
        elif username == 'admin' and password=='admin':
                return redirect('document-admin')  # Redirect to admin dashboard
            # else:
            #     return redirect('updates')
           
        else:
            return HttpResponse("username or password is incorrect!!!")
    return render(request,"login.html")


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         # Admin-specific login check
#         if username == 'admin' and password == 'admin':
#             user = authenticate(request, username=username, password=password)
#             if user is not None and user.is_staff:  # Ensure the user is an authenticated staff
#                 login(request, user)
#                 return redirect('admin_dashboard')  # Redirect to admin dashboard
#             else:
#                 return HttpResponse("Invalid admin credentials or unauthorized access.")
        
#         # Normal user login
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')  # Redirect to user dashboard/home

#         return HttpResponse("Username or password is incorrect!")  # Invalid credentials

#     return render(request, "login.html")

def submitform(request):
    try:
        if request.method=="post":
            name=str(request.POST.get['name'])
            reason=str(request.POST.get['reason'])
            email=str(request.POST.get['email'])
            phone=int(request.POST.get['phone'])
            finalans=name+reason+email+phone;
            data={
                'name':name,
                'reason':reason,
                'email':email,
                'phone':phone,
                'output':finalans
            }

      
            return HttpResponse(request)
    except:
        pass

def usersForms(request):
    finalans=0
    fn=userForms()
    data={'form':fn}
    try:
        if request.method=="post":
            name=str(request.POST.get('name'))
            reason=str(request.POST.get('reason'))
            email=str(request.POST.get('email'))
            phone=str(request.POST.get('phone'))
            finalans=name+reason+email+phone;
            data={
               'form':fn,
               'output':finalans
            }
            url="/employment/?output={}".format(finalans)

            return redirect(url)
    except:
            pass
    return render(request,"userform.html",data)

      

def usa(request):
    if request.method == 'POST':
        # form = ServiceDocumentForm(request.POST)
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            form.save()
            return redirect('usa')  
    else:
        # form = ServiceDocumentForm()
        form = DocumentForm()
    user_documents = Document.objects.filter(user=request.user)
    return render(request, 'usa.html', {'form': form})


def user_documents(request):
    user_document = Document.objects.filter(user=request.user)

    return render(request,'user_documents.html',{'document':user_documents})
# def usa(request):
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         print(f"user_id: {user_id}")  # Debugging statement
#         form = ServiceDocumentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('usa')
#     else:
#         form = ServiceDocumentForm()
#     return render(request, 'usa.html', {'form': form})

def updates(request):
    return render(request,"updates.html")

# def loggedin(request):
#     return render(request,"loggedin.html")

# 2222222222222222222222222222222222222222222222
# @login_required
# def loggedin(request):
#     # Get feedback for the logged-in user
#     feedbacks = Feedback.objects.filter(user=request.user)
#     return render(request, 'loggedin.html', {
#         'feedbacks': feedbacks,
#         'title': 'User Dashboard'
#     })
#222222222222222222222222222222222222222
# @login_required
# def user_dashboard(request):
#     user = request.user
#     feedbacks = Feedback.objects.filter(document__user=user)

#     # print(f"Retrieved feedbacks: {feedbacks}")


#     return render(request, 'loggedin.html', {
#         'title': 'User Dashboard',
#         'feedbacks': feedbacks,
#     })
def user_dashboard(request):
    user_documents = Document.objects.filter(user=request.user)
    for doc in user_documents:
        # Use feedback_set if related_name is not set, or use 'feedbacks' if related_name is 'feedbacks'
        doc_feedback = doc.feedback_set.all()  # or doc.feedbacks.all() if you defined related_name='feedbacks'
        doc.feedback = doc_feedback  # Adding feedback to each document object
    
    context = {'documents': user_documents}
    return render(request, 'user_dashboard.html', context)


def working(request):
    return render(request,"future.html")
# def courses(request):
#     return HttpResponse("coursepage")

# def coursesDetails(request,courseid):
#     return HttpResponse(courseid)



# Admin document review view222222222222222222
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def admin_document_review(request):
#     documents = Document.objects.all()
#     if request.method == 'POST':
#         feedback_form = FeedbackForm(request.POST)
#         if feedback_form.is_valid():
#             feedback = feedback_form.cleaned_data['feedback']
#             doc_id = request.POST.get('document_id')
#             document = get_object_or_404(Document, pk=doc_id)
#             document.feedback = feedback
#             document.save()
#             return redirect('admin_document_review')
#     else:
#         feedback_form = FeedbackForm()

#     return render(request, 'admin_review.html', {
#         'documents': documents,
#         'feedback_form': feedback_form
#     })






# # # 2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def admin_document_review(request):
#     documents = Document.objects.all()
#     if request.method == 'POST':
#         feedback_form = FeedbackForm(request.POST)
#         if feedback_form.is_valid():
#             doc_id = request.POST.get('document_id')
#             document = get_object_or_404(Document, pk=doc_id)
#             document.feedback = feedback_form.cleaned_data['feedback']
#             document.save()
#             return redirect('loggedin')
#     else:
#         feedback_form = FeedbackForm()

#     return render(request, 'loggedin.html', {
#         'documents': documents,
#         'feedback_form': feedback_form
#     })

# # Document feedback view
# # @login_required
# def admin_feedback(request, pk):
#     document = get_object_or_404(Document, pk=pk)
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             feedback = form.save(commit=False)
#             feedback.document = document
#             feedback.admin = request.user
#             feedback.save()
#             # Optionally notify the user (e.g., via email)
#             return redirect('loggedin')
#     else:
#         form = FeedbackForm()
#     return render(request, 'loggedin.html', {'document': document, 'feedback_form': form})


# # def admin_dashboard(request):
# #     documents = Document.objects.all()
# #     return render(request, 'admin.html', {'documents': documents, 'feedback_form': FeedbackForm()})

# # @login_required
# # def admin_dashboard(request):
# #     # if not request.user.is_staff:
# #     #     return redirect('de')  # Redirect non-admin users

# #     documents = Document.objects.all()
# #     feedback_form = FeedbackForm()

# #     if request.method == 'POST':
# #         form = FeedbackForm(request.POST)
# #         if form.is_valid():
# #             feedback_text = form.cleaned_data['feedback_text']
# #             document_id = form.cleaned_data['document_id']
# #             document = Document.objects.get(pk=document_id)
# #             Feedback.objects.create(
# #                 document=document,
# #                 admin=request.user,
# #                 user=document.user,
# #                 feedback_text=feedback_text
# #             )
# #             return redirect('document-admin')  # Redirect after successful feedback submission

# #     return render(request, 'admin.html', {
# #         'documents': documents,
# #         'feedback_form': feedback_form
# #     })

# @login_required
# def admin_dashboard(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             document_id = request.POST.get('document_id')
#             document = get_object_or_404(Document, pk=document_id)
#             document.feedback = form.cleaned_data['feedback']
#             document.save()
#             return redirect('document-admin')  # or your desired URL

#     documents = Document.objects.all()  # Adjust this as needed
#     feedback_form = FeedbackForm()  # Instantiate form for display

#     context = {
#         'title': 'document-admin',
#         'documents': documents,
#         'feedback_form': feedback_form,
#     }
#     return render(request, 'admin.html', context)
# # 22222222222222222222222222222222222222222222222222222222222222
def admin_dashboard(request):
    if request.method == 'POST':
     
        form = FeedbackForm(request.POST)
        if form.is_valid():
            document_id = request.POST.get('document_id')
            document = get_object_or_404(Document, pk=document_id)
            # document.feedback = form.cleaned_data['feedback']
            # document.save()
            feedback = form.cleaned_data['feedback']
            document.feedback = feedback
            document.save()

            Feedback.objects.create(
                document=document,
                admin=request.user,
                user=document.user,
                feedback_text=feedback
                # feedback_text=form.cleaned_data['feedback']
            )
            return redirect('document-admin')  # or your desired URL
        else:
            print(form.errors)

    documents = Document.objects.all()
    feedback_form = FeedbackForm()

    # context = {
    #     'title': 'Document Admin',
    #     'documents': documents,
    #     'feedback_form': feedback_form,
    # }
    return render(request, 'admin.html', {
        'documents': documents,
        'feedback_form': feedback_form,
    })
    return render(request, 'admin.html', context)
# 3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
# views.py

# @login_required
# def admin_dashboard(request):
#     if request.method == 'POST':
#         feedback_text = request.POST.get('feedback')
#         document_id = request.POST.get('document_id')
        
#         # Save the feedback to the database
#         document = Document.objects.get(id=document_id)
#         Feedback.objects.create(document=document, feedback_text=feedback_text)
        
#         # Optionally print feedback to the terminal
#         print(f"Feedback for Document ID {document_id}: {feedback_text}")

#         # Redirect back to the admin page
#         return redirect('admin_page')  # Replace 'admin_page' with the actual name of the URL pattern for your admin page

#     return redirect('admin_page')  # Hand

# def document_admin_feedback(request):
#     if request.method == 'POST':
#         feedback_text = request.POST.get('feedback')
#         document_id = request.POST.get('document_id')
        
#         # Save the feedback to the database
#         document = Document.objects.get(id=document_id)
#         Feedback.objects.create(document=document, feedback_text=feedback_text)
        
#         # Print feedback to terminal
#         print(f"Feedback for Document ID {document_id}: {feedback_text}")

#         # Redirect back to the admin page
#         return redirect('admin')  # Replace 'admin_page' with your actual URL name

#     return HttpResponse("Invalid request method.", status=405)

# @login_required
# def admin_dashboard(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             document_id = request.POST.get('document_id')
#             document = get_object_or_404(Document, pk=document_id)
#             feedback_text = form.cleaned_data['feedback_text']

            
#             # Create a new feedback entry
#             Feedback.objects.create(
#                 document=document,
#                 admin=request.user,
#                 user=document.user,
#                 feedback_text=feedback_text
#             )
            
#         return redirect('document-admin') 
       
 # Redirect after submission



# @login_required
# def admin_dashboard(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             document_id = request.POST.get('document_id')  # Get the document ID from the POST data
#             document = get_object_or_404(Document, pk=document_id)  # Fetch the document object
#             feedback_text = form.cleaned_data['feedback_text']  # Get feedback text from form

#             print(f"Creating feedback for document {document}, user {document.user}")
            
#             # Create a new feedback entry
#             Feedback.objects.create(
#                 document=document,
#                 admin=request.user,
#                 user=document.user,
#                 feedback_text=feedback_text  # Save feedback text
#             )
            
#             return redirect('document-admin')  # Redirect after saving feedback

#     # If it's not a POST request, display the dashboard with documents
#     documents = Document.objects.all()  # Fetch all documents
#     form = FeedbackForm()  # Instantiate an empty feedback form

# 444444444444444444444444444444444
# def document_admin(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             document_id = request.POST.get('document_id')
#             document = get_object_or_404(Document, pk=document_id)
#             document.feedback = form.cleaned_data['feedback']
#             document.save()
#             return redirect('document-admin')
#     else:
#         form = FeedbackForm()

#         documents = Document.objects.all()
#         return render(request, 'document_admin.html', {'documents': documents, 'form': form})
#     documents = Document.objects.all()
#     feedback_form = FeedbackForm()

#     context = {
#         'title': 'Document Admin',
#         'documents': documents,
#         'feedback_form': feedback_form,
#     }
#     return render(request, 'admin.html', context)




# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def admin_dashboard(request):
#     if request.method == 'POST':
#         feedback_form = FeedbackForm(request.POST)
#         if feedback_form.is_valid():
#             doc_id = request.POST.get('document_id')
#             document = get_object_or_404(Document, pk=doc_id)
#             document.feedback = feedback_form.cleaned_data['feedback']
#             document.save()
#             return redirect('admin')  # Redirect to the same page to refresh feedback

#     documents = Document.objects.all()
#     feedback_form = FeedbackForm()

#     context = {
#         'title': 'Document Admin Dashboard',
#         'documents': documents,
#         'feedback_form': feedback_form,
#     }
#     return render(request, 'admin.html', context)
















# def admin_dashboard(request):
#     if request.method == 'POST':
#         # Get feedback from the form
#         feedback = request.POST.get('feedback')
#         document_id = request.POST.get('document_id')

#         if feedback is not None and document_id:
#             try:
#                 # Fetch the document by its ID
#                 document = Document.objects.get(id=document_id)
#                 # Save the feedback to the document
#                 document.feedback = feedback
#                 document.save()
#                 messages.success(request, "Feedback submitted successfully.")
#             except Document.DoesNotExist:
#                 messages.error(request, "Document not found.")
#         else:
#             messages.error(request, "Feedback or document ID is missing.")

#     return render(request, 'admin.html')

# def admin_dashboard(request):
#     if request.method == 'POST':
#         # Safely get 'feedback' from the POST data
#         feedback = request.POST.get('feedback', '')  # Default to an empty string if 'feedback' is not found

#         # Process the feedback and update the Document model or other logic
#         try:
#             # Assuming you're associating the feedback with a specific document
#             document_id = request.POST.get('document_id')
#             document = Document.objects.get(id=document_id)
#             document.feedback = feedback
#             document.save()
#             messages.success(request, "Feedback submitted successfully.")
#         except Document.DoesNotExist:
#             messages.error(request, "Document not found.")
#         except Exception as e:
#             messages.error(request, f"An error occurred: {str(e)}")

    # Handle GET request or render template
   
    return render(request, 'admin.html')




@login_required
def user_dashboard(request):
    documents = Document.objects.filter(user=request.user)
    print("Documents:", documents) 
    feedbacks = Feedback.objects.filter(document__in=documents)
    print("Feedbacks:", feedbacks)

    return render(request, 'loggedin.html', {
        'documents': documents,
        'feedbacks': feedbacks
    })


# ///////////////////////////////cfor API and receomendation system
# def education(request):
#    return render(request,"education.html")
# def unirecomend(request):
#     return render(request,"unirecomend.html")


# def education(request):
#     if request.method == 'POST':
#         user_city = request.POST['city']
#         user_country = request.POST['country']
#         user_cost = int(request.POST['cost'])
#         user_subjects = request.POST['subjects']
#         user_ielts_score = float(request.POST['ielts'])
        
#         # Make API call to Flask app
#         api_url = 'http://<flask_server_ip>:5000/api/recommend'
#         payload = {
#             'city': user_city,
#             'country': user_country,
#             'cost': user_cost,
#             'subjects': user_subjects,
#             'ielts': user_ielts_score
#         }
#         response = requests.post(api_url, json=payload)
        
#         # Process the API response
#         if response.status_code == 200:
#             recommendations = response.json()
#             return render(request, 'unirecomend.html', {'recommendations': recommendations})
#         else:
#             return render(request, 'education.html', {'error': 'Unable to fetch recommendations at this time.'})
    
#     return render(request, 'education.html')
def education(request):
   return render(request,"education.html")

# def university_recommendation_view(request):
#     if request.method == 'POST':
#         user_city = request.POST['city']
#         user_country = request.POST['country']
#         user_cost = int(request.POST['cost'])
#         user_subjects = request.POST['subjects']
#         user_ielts_score = float(request.POST['ielts'])
        
#         # Prepare data for API call
#         data = {
#             'city': user_city,
#             'country': user_country,
#             'cost': user_cost,
#             'subjects': user_subjects,
#             'ielts': user_ielts_score
#         }
        
#         # Make the API call to Flask
#         response = requests.post('http://127.0.0.1:5000/api/recommend', json=data)
        
#         # Handle the response from Flask API
#         if response.status_code == 200:
#             recommendations = response.json()
#             return render(request, 'unirecomend.html', {'recommendations': recommendations})
#         else:
#             return render(request, 'education.html', {'error': 'Failed to get recommendations'})
    
#     return render(request, 'education.html')