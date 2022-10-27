from django.shortcuts import render, redirect
from distutils.log import Log
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from numpy import is_busday
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse

class Postlist(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'single_pages/index.html'

class PostDetail(DetailView):
    model = Post
    
class administ(ListView, UserPassesTestMixin):
    model = Post
    template_name = 'single_pages/ad.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'hook_test', 'content', 'head_image', 'file_upload', 'category']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(requset, *args, **kwargs)
        else:
            raise PermissionDenied

# 오류나면 원인중 하나일 예정
def index(request):
    return HttpResponse("기본요청 처리")

def hello_func(request):
    msg = '장고 '
    ss = "<html><body>장고프로젝트 작성 메세지 : %s</body></html>"%msg
    return HttpResponse(ss)

def hello_template(request):
    mymsg = '홍길동'
    return render(request, 'show.html',{'msg':mymsg})

def world_func(request):
    return render(request, 'disp.html')


# def index(request):
#     return render(
#         request,
#         'single_pages/index.html'
#     )
