from django.contrib import admin
from django.urls import path
from pdf import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accept, name="accept"),
    path('<int:id>/', views.resume, name="resume"),
    path('list/', views.list, name="list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
