from django.db import models

class ImageUpload(models.Model):
    # файли будуть зберігатися в папці MEDIA_ROOT/images/
    image = models.ImageField(upload_to='images/')
    classification_result = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at} ({self.classification_result[:20]}...)"
    

class VideoUpload(models.Model):
    video_file = models.FileField(upload_to='videos/%Y/%m/%d/')
    analysis_result = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video {self.id} uploaded at {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    
class AudioUpload(models.Model):
    """Модель для зберігання аудіофайлів та результатів їх аналізу."""
    audio_file = models.FileField(upload_to='audio_uploads/')
    analysis_result = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio: {self.audio_file.name}"


class SignalUpload(models.Model):
    """Зберігає сирий сигнал (аудіо або WAV/MP3) і результат спектрального аналізу."""
    signal_file = models.FileField(upload_to='signal_uploads/')
    spectrum_summary = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Signal #{self.id} at {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class TextUpload(models.Model):
    """Завантаження текстового файлу та аналіз читабельності."""
    input_file = models.FileField(upload_to='text_uploads/', blank=True, null=True)
    input_text = models.TextField(blank=True)
    readability_score = models.FloatField(blank=True, null=True)
    verdict = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TextUpload #{self.id} ({self.verdict})"


