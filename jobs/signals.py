from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job, Subscriber
from django.template.loader import render_to_string
from .tasks import send_job_email


@receiver(post_save, sender=Job)
def send_new_job_email(sender, instance, created, **kwargs):
    if created:
        subscribers = Subscriber.objects.all()

        for sub in subscribers:

            html_content = render_to_string(
                "emails/new_jobs.html",
                {"jobs": [instance]}
            )

            send_job_email.delay(
                subject=f"🔥 New Job: {instance.title}",
                message=html_content,
                recipients=[sub.email]
            )