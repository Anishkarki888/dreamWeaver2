"""
URL configuration for dreamweavers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dreamweavers import views
from django.conf import settings
from django.conf.urls.static import static
from recommendation.views import university_recommendation_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('education/', views.education,name='education'),
    path('employment/', views.employment,name='employment'),
    path('apply/', views.apply,name='apply'),
    path('signup/', views.signup,name='signup'),
    path('login/', views.login_view,name='login'),
    path('submitform/', views.submitform,name='submitform'),
    path('userform/', views.usersForms,name='userform'),
    path('usa/', views.usa,name='usa'),
    path('updates/', views.updates,name='updates'),
    # path('loggedin/', views.loggedin,name='loggedin'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('working/', views.working,name='working'),
    path('user-document/', views.user_documents,name='user_documents'),
    # path('admin/review/', views.admin_document_review, name='admin_document_review'),
    path('document-admin/', views.admin_dashboard, name='document-admin'),
    # path('document/feedback/<int:pk>/', views.admin_feedback, name='document_feedback'),
    path('recommendations', university_recommendation_view, name='university_recommendation'),
    # path('course/', views.courses),
    # path('course/<str:courseid>', views.coursesDetails),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
