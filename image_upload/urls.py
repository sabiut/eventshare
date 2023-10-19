from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('delete_image/<int:image_id>/',
         views.delete_image, name='delete_image'),
]
