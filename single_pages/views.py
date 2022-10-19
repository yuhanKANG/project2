from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

class Postlist(ListView):
    model = Post
    ordering = '-pk'
# def index(request):
#     return render(
#         request,
#         'single_pages/index.html'
#     )
