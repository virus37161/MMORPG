from django_filters import FilterSet, DateFilter, ModelMultipleChoiceFilter,CharFilter,ModelChoiceFilter
from .models import Post, Category, Responses, User
from django import forms

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ResponseFilter(FilterSet):
    class Meta:
        model = Responses
        fields = ['response_post']

    def __init__(self, *args, **kwargs):
        super(ResponseFilter, self).__init__(*args, **kwargs)
        self.filters['response_post'].queryset = Post.objects.filter(post_user_id = kwargs['request'])