from django.urls import path, include
from .views import *
urlpatterns = [
    path('post/', PostList.as_view(), name = 'post_list'),
    path('post/<int:pk>/', PostDetail.as_view()),
    path('post/create/', PostCreate.as_view()),
    path('post/delete/<int:pk>/', PostDelete.as_view()),
    path('post/update/<int:pk>/', PostUpdate.as_view()),
    path('post/response/<int:pk>/', response_add),
    path('post/response_list/', ResponseList.as_view()),
    path('post/response_delete/<int:pk>/', response_delete),
    path('post/response_confirm/<int:pk>/', response_confirm)
]