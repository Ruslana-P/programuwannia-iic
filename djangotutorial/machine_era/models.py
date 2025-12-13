from django.db import models

class ImageUpload(models.Model):
    # Поле для збереження самого файлу зображення. 
    # upload_to='images/' означає, що файли будуть зберігатися в папці MEDIA_ROOT/images/
    image = models.ImageField(upload_to='images/')

    # Поле для збереження результату, отриманого від моделі AI
    classification_result = models.CharField(max_length=255, blank=True, null=True)

    # Час завантаження
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at} ({self.classification_result[:20]}...)"