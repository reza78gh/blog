from django.urls import path ,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'weblog'
urlpatterns = [
    path('', views.home, name="home"),
    path('tag/<int:pk>/', views.home, {'mode':"tag"}, name="tag"),
    path('category/<int:pk>/', views.home, {'mode':"category"}, name="category"),
    path('new-post/', views.new_post, name="new_post"),
    path("accounts/",include('django.contrib.auth.urls')),
    path('register/', views.register, name="register"),
    path('add-comment/<int:post_id>/', views.add_comment, name="add_comment"),
    path('post/<int:pk>/', views.DetailPostView.as_view(), name="detail_post"),
    path('search/', views.search, name="search"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
