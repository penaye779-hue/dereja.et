from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job, Subscriber
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@receiver(post_save, sender=Job)
def send_new_job_email(sender, instance, created, **kwargs):
    if created:
        subscribers = Subscriber.objects.all()

        for sub in subscribers:
            html_content = render_to_string(
                "emails/new_jobs.html",
                {"jobs": [instance]}
            )

            email = EmailMultiAlternatives(
                subject=f"🔥 New Job: {instance.title}",
                body="New job posted",
                from_email=settings.EMAIL_HOST_USER,
                to=[sub.email],
            )

            email.attach_alternative(html_content, "text/html")
            email.send()