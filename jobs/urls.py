from django.urls import path
from . import views

urlpatterns = [

    # MAIN
    path('', views.job_list, name='job_list'),

    # STATIC PAGES
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),

    # NEWSLETTER
    path("send-newsletter/", views.send_newsletter),

    # SAVE JOBS
    path('jobs/save/<int:job_id>/', views.toggle_save_job, name='save_job'),
    path("jobs/saved/", views.saved_jobs, name="saved_jobs"),

    # CV SYSTEM
    path("cv-builder/", views.cv_builder, name="cv_builder"),
    path("cv-download/", views.download_cv, name="download_cv"),

    # 🔥 ALWAYS LAST (dynamic)
    path('<int:job_id>/', views.job_detail, name='job_detail'),
]