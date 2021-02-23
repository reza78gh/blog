from django.urls import path 
from . import views


app_name = 'api'
urlpatterns = [
    path('like-by-post/<int:pk>', views.LikePostList.as_view(),name='like-by-post'),
    path('like-post/<int:pk>', views.DetailLikePost.as_view(),name='detail-like-post'),
    path('like-post/', views.AddLikePost.as_view(),name='add-like-post'),
    path('comment/creata/', views.CommentCreateVeiw.as_view(),name='add-comment'),
]

