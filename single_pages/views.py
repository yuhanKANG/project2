from django.shortcuts import render, redirect
from distutils.log import Log
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin

class Postlist(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'single_pages/index.html'

class PostDetail(DetailView):
    model = Post
    

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'hook_test', 'content', 'head_image', 'file_upload', 'category']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/single_pages/')







# def index(request):
#     return render(
#         request,
#         'single_pages/index.html'
#     )
