from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import New


@receiver(post_save, sender=New)
def new_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__news=instance.news
    ).values_list('email', flat=True)

    subject = f'Новая новось уже на нашем сайте! {instance.news}'

    text_content = (
        f'Тема: {instance.name}\n'
        f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Тема: {instance.name}<br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на новость</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()