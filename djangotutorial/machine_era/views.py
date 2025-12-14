# djangotutorial/image_classifier/views.py
from django.shortcuts import render, redirect
from .models import ImageUpload, VideoUpload
from .ai_model import classify_image 
import os
from django.conf import settings
from .forms import ImageUploadForm, VideoUploadForm
from .ai_video_model import analyze_video 

def main_dashboard(request):
    """
    Відображає головну сторінку, яка служить меню для п'яти модулів.
    """
    modules = [
        {'id': 1, 'name': 'IMAGE RECOGNITION (Module Alpha)', 'url_name': 'image_upload'},       
        {'id': 2, 'name': 'VIDEO ELEMENT SCAN (Module Beta)', 'url_name': 'video_upload'}, 
        
        # Використовуємо 'dashboard' як заглушку для ще нереалізованих модулів, щоб уникнути помилок
        {'id': 3, 'name': 'AUDIO SIGNATURE ANALYSIS (Module Gamma)', 'url_name': 'dashboard'}, 
        {'id': 4, 'name': 'SIGNAL SPECTRUM DECODE (Module Delta)', 'url_name': 'dashboard'},  
        {'id': 5, 'name': 'CUSTOM AI VARIANT (Module Epsilon)', 'url_name': 'dashboard'},    
    ]
    
    context = {'modules': modules}
    return render(request, 'machine_era/dashboard.html', context)


# ---------- IMAGE RECOGNITION LOGIC -------------
def upload_and_classify_image(request):
    form = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            
            try:
                instance.save() 
                image_path = instance.image.path
                result = classify_image(image_path) 
                instance.classification_result = f"> CLASSIFICATION.RESULT: {result}" 
                
            except ImportError as e:
                instance.classification_result = f"[ERROR] DEPENDENCY.MISSING: {e.__class__.__name__}"
            except Exception as e:
                instance.classification_result = f"[EXECUTION.ERROR] {e.__class__.__name__}: {str(e)}"
            
            instance.save() 
            
            return redirect('machine_era:results') 
    else:
        form = ImageUploadForm()
            
    return render(request, 'machine_era/image_upload.html', {'form': form})


def classification_results(request):
    uploads = ImageUpload.objects.all().order_by('-uploaded_at')[:5] 
    return render(request, 'machine_era/image_results.html', {'uploads': uploads})


# ---------- VIDEO RECOGNITION LOGIC -------------
def upload_and_analyze_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save() 
            video_path = instance.video_file.path

            try:
                result = analyze_video(video_path)
                instance.analysis_result = f"> VIDEO.ANALYSIS.RESULT: {result}"

            except Exception as e:
                instance.analysis_result = f"[EXECUTION.ERROR] Video analysis failed: {str(e)}"

            instance.save()
            return redirect('machine_era:video_results')
    else:
        form = VideoUploadForm()
            
    return render(request, 'machine_era/video_upload.html', {'form': form})

def video_analysis_results(request):
    uploads = VideoUpload.objects.all().order_by('-uploaded_at')[:5] 
    return render(request, 'machine_era/video_results.html', {'uploads': uploads})