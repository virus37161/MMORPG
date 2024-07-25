from django_filters import FilterSet, DateFilter, ModelMultipleChoiceFilter,CharFilter,ModelChoiceFilter
from .models import Post, Category
from django import forms

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ResponseFilter(FilterSet):
    name = CharFilter (lookup_expr = 'icontains', field_name = "name", label = 'Название')
    category = ModelChoiceFilter(field_name = 'post_category', queryset = Category.objects.all(), label = 'Категории')

    class Meta:
        model = Post
        fields = ['name']