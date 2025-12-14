from .ai_model import MODEL, decode_predictions_local 
from tensorflow.keras.applications.vgg16 import preprocess_input

def get_vgg16_model_and_decoder():
    """
    Повертає завантажену VGG16 модель та локальну функцію декодування.
    """
    # Перевіряємо, чи була модель успішно ініціалізована в ai_model.py
    if MODEL is None:
        raise Exception("VGG16 model failed to initialize in ai_model.py.")
        
    return MODEL, decode_predictions_local