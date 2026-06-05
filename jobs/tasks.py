from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task
def send_job_email(subject, message, recipients):

    email = EmailMultiAlternatives(
        subject=subject,
        body="New job posted",
        from_email=settings.EMAIL_HOST_USER,
        to=recipients,
    )

    email.attach_alternative(message, "text/html")
    email.send()