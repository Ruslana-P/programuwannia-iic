# djangotutorial/image_classifier/views.py
from django.shortcuts import render, redirect
from .models import ImageUpload

# Імпорт AI-функції
from .ai_model import classify_image 
import os
from django.conf import settings
from .forms import ImageUploadForm 

def main_dashboard(request):
    """
    Відображає головну сторінку, яка служить меню для п'яти модулів.
    """
    modules = [
        {'id': 1, 'name': 'IMAGE RECOGNITION (Module Alpha)', 'url': '/image-classifier/'},
        {'id': 2, 'name': 'VIDEO ELEMENT SCAN (Module Beta)', 'url': '/machine-era/video-scan/'},
        {'id': 3, 'name': 'AUDIO SIGNATURE ANALYSIS (Module Gamma)', 'url': '/machine-era/audio-analyze/'},
        {'id': 4, 'name': 'SIGNAL SPECTRUM DECODE (Module Delta)', 'url': '/machine-era/spectrum-decode/'},
        {'id': 5, 'name': 'CUSTOM AI VARIANT (Module Epsilon)', 'url': '/machine-era/custom-module/'},
    ]
    
    context = {'modules': modules}
    return render(request, 'machine_era/dashboard.html', context)

# Проста форма для завантаження файлу, що базується на моделі ImageUpload

# def upload_and_classify_image(request):
#     # Спочатку визначаємо змінну form, щоб уникнути помилки.
#     form = None # Ініціалізуємо змінну 'form'

#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # ... (логіка обробки POST-запиту) ...
#             # ... (ТУТ ВИКЛИК AI CLASSIFY_IMAGE) ...
#             return redirect('machine_era:results') 
#     else:
#         # Якщо GET-запит (відкриття сторінки), створюємо порожню форму
#         form = ImageUploadForm()
            
#     # Цей рядок тепер безпечний, оскільки 'form' завжди визначена
#     return render(request, 'machine_era/upload.html', {'form': form})

# djangotutorial/machine_era/views.py

# ... (переконайтеся, що імпорт є: from .ai_model import classify_image) ...

def upload_and_classify_image(request):
    form = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            
            try:
                # 1. Зберігаємо інстанс, щоб отримати шлях
                instance.save() 
                image_path = instance.image.path
                
                # ----------------------------------------------------------------------
                # !!! ВАЖЛИВО: ВІДНОВЛЮЄМО ВИКЛИК AI !!!
                # 2. Викликаємо функцію класифікації
                result = classify_image(image_path) 
                
                # 3. Зберігаємо реальний результат
                instance.classification_result = f"> CLASSIFICATION.RESULT: {result}" 
                # ----------------------------------------------------------------------
                
            except ImportError as e:
                instance.classification_result = f"[ERROR] DEPENDENCY.MISSING: {e.__class__.__name__}"
            except Exception as e:
                # Загальна помилка при виконанні classify_image
                instance.classification_result = f"[EXECUTION.ERROR] {e.__class__.__name__}: {str(e)}"
            
            # Зберігаємо результат (навіть якщо це помилка)
            instance.save() 
            
            # Перенаправляємо на сторінку результатів
            return redirect('machine_era:results') 
    else:
        # GET-запит
        form = ImageUploadForm()
            
    return render(request, 'machine_era/upload.html', {'form': form})

def classification_results(request):
    # Отримання останніх 5 завантажених зображень
    uploads = ImageUpload.objects.all().order_by('-uploaded_at')[:5] 
    return render(request, 'machine_era/results.html', {'uploads': uploads})