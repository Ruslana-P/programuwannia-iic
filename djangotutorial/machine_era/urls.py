# djangotutorial/machine_era/urls.py

from django.urls import path
from . import views

app_name = 'machine_era' 

urlpatterns = [
    path('', views.main_dashboard, name='dashboard'), 
    
    # image recognition module
    path('image-upload/', views.upload_and_classify_image, name='image_upload'), # Тепер це /machine-era/image-classify/
    path('image_results/', views.classification_results, name='image_results'),
    
    # video recognition module
    path('video-scan/', views.upload_and_analyze_video, name='video_upload'),
    path('video-results/', views.video_analysis_results, name='video_results'),


]