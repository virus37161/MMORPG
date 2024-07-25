from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
import datetime
from .models import User



@shared_task
def send_week():
    last_date = datetime.datetime.today()
    first_date = last_date - datetime.timedelta(days=7)
    for user in User.objects.all():
        email = user.email
        content = []
        for i in Post.objects.filter(some_data__gte = first_date, some_data__lte = last_date).all():
            content.append(i)
        html_content = render_to_string(
            'email_send_week.html',
            {
                'content': content
            })
        msg = EmailMultiAlternatives(
            subject=f'Недельная рассылка',
            body=f"Список новостей за неделю",
            from_email='unton.edgar.2001@yandex.ru',
            to=[f'{email}'],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()