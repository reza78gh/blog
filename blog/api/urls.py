from django.urls import path 
from . import views


app_name = 'api'
urlpatterns = [
    path('like-by-post/<int:pk>', views.LikePostList.as_view(),name='like-by-post'),
    path('like-post/<int:pk>', views.DetailLikePost.as_view(),name='detail-like-post'),
    path('like-post/', views.AddLikePost.as_view(),name='add-like-post'),
    path('like-by-comment/<int:pk>', views.LikeCommentList.as_view(),name='like-by-comment'),
    path('like-comment/<int:pk>', views.DetailLikeComment.as_view(),name='detail-like-comment'),
    path('like-comment/', views.AddLikeComment.as_view(),name='add-like-comment'),
    path('comment/creata/', views.CommentCreateVeiw.as_view(),name='add-comment'),
    path('category/', views.CategoryList.as_view(),name='categotis'),
]

