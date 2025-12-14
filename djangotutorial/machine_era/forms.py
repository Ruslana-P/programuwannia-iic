# djangotutorial/machine_era/forms.py
from django import forms
from .models import ImageUpload, VideoUpload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ('video_file',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # === ДОДАЄМО АТРИБУТ 'accept' ===
        self.fields['video_file'].widget.attrs.update({
            # Поширені відеоформати: MP4, MOV, WebM, OGG
            'accept': 'video/mp4,video/quicktime,video/webm,video/ogg', 
        })

# DATA_UPLOAD_MAX_MEMORY_SIZE =  2.5 Мегабайта -deafult django limit
# Ваша функція analyze_video (з OpenCV та, можливо, YOLO) працює, обробляючи відео кадр за кадром.

#     Відео 10 секунд @ 30 FPS = 300 кадрів.

#     Відео 5 хвилин @ 30 FPS = 9000 кадрів.

# Якщо обробка одного кадру займає 0.5 секунди (це багато), 5-хвилинне відео займе 9000×0.5 секунд, тобто 4500 секунд, або 75 хвилин!