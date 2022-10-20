from django.views.generic import ListView, DetailView
from .models import Post

class Postlist(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'single_pages/index.html'

class PostDetail(DetailView):
    model = Post
    
# def index(request):
#     return render(
#         request,
#         'single_pages/index.html'
#     )
