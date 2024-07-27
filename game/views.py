from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView,TemplateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from .filters import ResponseFilter

class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'data'

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class PostCreate(LoginRequiredMixin,CreateView):
    form_class= PostForm
    model = Post
    template_name = "post_create.html"
    success_url = '/post/'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_user_id = self.request.user.id
        self.object = form.save()
        return super().form_valid(form)

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    def form_valid(self, form):
        success_url = self.get_success_url()
        if self.object.post_user_id == self.request.user.id:
            self.object.delete()
        else:
            return HttpResponseRedirect("Invalid Url")
        return HttpResponseRedirect(success_url)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    def form_valid(self,form):
        if self.object.post_user_id == self.request.user.id:
            self.object = form.save()
        else:
            return HttpResponseRedirect("Invalid Url")
        return super().form_valid(form)


@login_required
def response_add (request, pk):

    message = request.POST['my_input']
    user = request.user
    post = Post.objects.get(id = pk)
    user_take = User.objects.get(id=post.post_user_id)
    if user.id != post.post_user_id:
        Responses.objects.create(response_post_id = post.id, response_user_id = user.id, message = message)
    return redirect('/post')

class ResponseList(LoginRequiredMixin,ListView):
    model = Responses
    template_name = 'response_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        queryset = Responses.objects.filter(response_post__post_user_id = self.request.user.id)
        self.filterset = ResponseFilter(self.request.GET, queryset, request = self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        else:
            return Responses.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

@login_required
def response_delete (request,pk):
    user = request.user
    response = Responses.objects.get(id=pk)
    post = Post.objects.get (id = response.response_post_id)
    if post.post_user_id == user.id:
        response.delete()
    return redirect('/post/response_list/')

@login_required
def response_confirm(request, pk):
    user = request.user
    response = Responses.objects.get(id = pk)
    user_take = User.objects.get(id = response.response_user_id)
    post = Post.objects.get(id=response.response_post_id)
    if post.post_user_id == user.id:
        html_content = render_to_string(
            'email_response_confirm.html',
            {
                'data': user_take.username,
                'post': post.name
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'Добрый день, {user_take.username}!',
            body=f'Добрый день, {user_take.username} ',  # это то же, что и message
            from_email='unton.edgar.2001@yandex.ru',
            to=[f'{user_take.email}'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем
        response.delete()
        return redirect('/post/response_list/')


