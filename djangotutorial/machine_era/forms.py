from django import forms
from .models import ImageUpload, VideoUpload, AudioUpload, SignalUpload, TextUpload


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']
        widgets = {
            'image': forms.FileField.widget(attrs={
                'accept': 'image/*'
            }),
        }


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ('video_file',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['video_file'].widget.attrs.update({
            'accept': 'video/mp4,video/quicktime,video/webm,video/ogg', 
        })


class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioUpload
        fields = ('audio_file',)
        widgets = {
            'audio_file': forms.FileField.widget(attrs={
                'class': 'protocol-file-input',
                'accept': 'audio/*' 
            }),
        }


class SignalUploadForm(forms.ModelForm):
    class Meta:
        model = SignalUpload
        fields = ('signal_file',)
        widgets = {
            'signal_file': forms.FileField.widget(attrs={
                'class': 'protocol-file-input',
                'accept': 'audio/*',
            }),
        }


class TextUploadForm(forms.ModelForm):
    class Meta:
        model = TextUpload
        fields = ('input_file',)
        widgets = {
            'input_file': forms.FileField.widget(attrs={
                'class': 'protocol-file-input',
                'accept': '.txt,.md,.csv,.log,text/plain',
            }),
        }


