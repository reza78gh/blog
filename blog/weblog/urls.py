from django.urls import path ,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'weblog'
urlpatterns = [
    path('', views.home, name="home"),
    path('new-post/', views.new_post, name="new_post"),
    path("accounts/",include('django.contrib.auth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
