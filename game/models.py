from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    name_category = models.TextField(unique= True)

    def __str__(self):
        return f'{self.name_category.title()}'

class User(AbstractUser):
    code = models.CharField(max_length=15, blank = True, null = True)

class Post(models.Model):
    post_user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Пользователь')
    name = models.TextField(verbose_name='Название')
    text = RichTextUploadingField(verbose_name='Текст')
    post_category = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.name.title()}'

class Responses(models.Model):
    response_user = models.ForeignKey(User, on_delete = models.CASCADE)
    response_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField(verbose_name = 'Сообщение', default="")

class Codes(models.Model):
    username = models.TextField()
    code = models.IntegerField()

