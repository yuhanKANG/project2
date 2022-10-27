from django.urls import path
from . import views

urlpatterns = [
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.Postlist.as_view()),
    path('ad/', views.administ.as_view()),
    # path('', views.index),
    # path('<int:pk>/', views.single_post_page),
]