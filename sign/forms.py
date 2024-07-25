from allauth.account.forms import SignupForm
from string import hexdigits
import random


from django.core.mail import send_mail

class CommonSignupForm(SignupForm):
    def save(self,request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email = 'unton.edgar.2001@yandex.ru',
            recipient_list = [user.email],
        )
        return user