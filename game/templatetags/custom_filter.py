from django import template
from game.models import User

register = template.Library()


@register.filter()
def name_user(a):
    name = User.objects.get(id=a.response_user_id)
    return name.username