from django.urls import path ,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'weblog'
urlpatterns = [
    path('', views.home, name="home"),
    path('<int:category_id>', views.home, name="category"),
    path('new-post/', views.new_post, name="new_post"),
    path("accounts/",include('django.contrib.auth.urls')),
    path('register/', views.register, name="register"),
    path('add-comment/<int:post_id>', views.add_comment, name="add_comment"),
    path('like/<int:post_id>/<int:value>', views.like, name="like"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
