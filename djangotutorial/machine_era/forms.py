# djangotutorial/machine_era/forms.py
from django import forms
from .models import ImageUpload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']
    # ... (ініціалізація, як ми додали для стилю) ...