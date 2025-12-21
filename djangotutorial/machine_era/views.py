from django.shortcuts import render, redirect
from .models import ImageUpload, VideoUpload, AudioUpload, SignalUpload
from .ai_model import classify_image 
import os
from django.conf import settings
from .forms import ImageUploadForm, VideoUploadForm, AudioUploadForm, SignalUploadForm
from .ai_video_model import analyze_video 
from .ai_audio_model import analyze_audio
from .ai_spectrum_model import analyze_signal_spectrum
from django.core.files.storage import FileSystemStorage
from .models import AudioUpload

def main_dashboard(request):
    """
    Відображає головну сторінку, яка служить меню для п'яти модулів.
    """
    modules = [
        {'id': 1, 'name': 'IMAGE RECOGNITION (Module Alpha)', 'url_name': 'image_upload'},       
        {'id': 2, 'name': 'VIDEO ELEMENT SCAN (Module Beta)', 'url_name': 'video_upload'}, 
        {'id': 3, 'name': 'AUDIO SIGNATURE ANALYSIS (Module Gamma)', 'url_name': 'audio_upload'},
        {'id': 4, 'name': 'SIGNAL SPECTRUM DECODE (Module Delta)', 'url_name': 'signal_upload'},

        # Використовуємо 'dashboard' як заглушку для ще нереалізованих модулів, щоб уникнути помилок
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
            
            return redirect('machine_era:image_results') 
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



# ---------- AUDIO RECOGNITION LOGIC -------------
def upload_and_analyze_audio(request):
    """Приймає аудіофайл, аналізує його та зберігає результат у базу даних."""
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Збереження об'єкта AudioUpload з файлом
            new_audio_upload = AudioUpload(audio_file=request.FILES['audio_file'])
            new_audio_upload.save()

            # 2. Виконання аналізу
            full_path = new_audio_upload.audio_file.path 
            analysis_result = analyze_audio(full_path)
            
            # 3. Збереження результату аналізу в БД
            new_audio_upload.analysis_result = analysis_result
            new_audio_upload.save()

            # 4. Перенаправлення на сторінку результатів
            return redirect('machine_era:audio_results')
            
    else:
        form = AudioUploadForm()
        
    return render(request, 'machine_era/audio_upload.html', {'form': form})


def audio_analysis_results(request):
    """Відображає всі результати аудіоаналізу з бази даних."""
    # Отримати всі записи з бази даних, сортуючи за часом створення (від найновіших)
    audio_uploads = AudioUpload.objects.all().order_by('-uploaded_at')

    return render(request, 'machine_era/audio_result.html', {
        'audio_uploads': audio_uploads
    })


def upload_and_analyze_signal(request):
    """
    Модуль Delta: завантаження сигналу та розшифровка спектру (FFT).
    """
    if request.method == 'POST':
        form = SignalUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance: SignalUpload = form.save()
            try:
                result = analyze_signal_spectrum(instance.signal_file.path)
                instance.spectrum_summary = result["summary"]
                instance.save()
            except Exception as exc:
                instance.spectrum_summary = f"[SPECTRUM.ERROR] {exc.__class__.__name__}: {exc}"
                instance.save()
            return redirect('machine_era:signal_results')
    else:
        form = SignalUploadForm()

    return render(request, 'machine_era/signal_upload.html', {'form': form})


def signal_spectrum_results(request):
    """
    Відображає останні результати спектрального аналізу.
    """
    uploads = SignalUpload.objects.all().order_by('-uploaded_at')[:10]
    return render(request, 'machine_era/signal_results.html', {'uploads': uploads})
