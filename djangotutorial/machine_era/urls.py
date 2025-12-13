# djangotutorial/machine_era/urls.py

from django.urls import path
from . import views

# ВАЖЛИВО: Оновлюємо app_name на нову назву додатку
app_name = 'machine_era' 

urlpatterns = [
    # 1. Головна Панель (Новий маршрут)
    path('', views.main_dashboard, name='dashboard'), 
    
    # 2. Модуль Розпізнавання Зображення (Перейменований)
    path('image-classify/', views.upload_and_classify_image, name='upload'), # Тепер це /machine-era/image-classify/
    path('results/', views.classification_results, name='results'),
    
    # 3. Маршрути для майбутніх модулів (поки що не реалізовані)
    path('video-scan/', views.main_dashboard, name='video_scan'),
    path('audio-analyze/', views.main_dashboard, name='audio_analyze'),
    # ...
]