from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


@receiver(post_save, sender=Responses)
def email_response (sender, instance, created, **kwargs):
    post = Post.objects.get(id = instance.response_post_id)
    user_take = User.objects.get(id = post.post_user_id)
    username = user_take.username
    email = user_take.email
    name = post.name
    message = instance.message
    html_content = render_to_string(
        'email_response.html',
        {
            'data': username,
            'post': name,
            'message': message
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Добрый день, {username}!',
        body=f'Добрый день, {username}! ',  # это то же, что и message
        from_email='unton.edgar.2001@yandex.ru',
        to=[f'{email}'],  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем
