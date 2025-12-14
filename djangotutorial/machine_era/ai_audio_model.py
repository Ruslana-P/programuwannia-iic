import numpy as np
import os
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from collections import Counter
from django.conf import settings 
from pydub import AudioSegment   
import tensorflow_hub as hub
import csv

SAMPLE_RATE = 22050        
N_MFCC = 13            
DURATION = 5              

def analyze_audio(audio_path):
    """
    Основна функція для аналізу аудіо та розпізнавання звукової події.
    """
    if not os.path.exists(audio_path):
        return "ANALYSIS.OUTPUT: CRITICAL.ERROR: Audio file not found."
        
    model = get_audio_model()
    if model is None:
        # Помилка завантаження моделі
        return "ANALYSIS.OUTPUT: CRITICAL.ERROR: Audio model not loaded. Check server logs."
        
    # 1. Екстракція характеристик
    mfcc_features = extract_mfcc(audio_path)
    
    if mfcc_features is None:
        return "ANALYSIS.OUTPUT: CRITICAL.ERROR: Failed to process audio features. Check file format/ffmpeg."

    try:
        # --- РЕАЛЬНА ЛОГІКА ПРОГНОЗУВАННЯ З TENSORFLOW ---
        # 1. Зміна форми для входу моделі ([1, N_FEATURES])
        mfcc_input = mfcc_features.reshape(1, -1) 
        
        # 2. Передбачення
        predictions = model.predict(mfcc_input, verbose=0)
        
        # 3. Отримання індексу класу з найбільшою ймовірністю
        predicted_index = np.argmax(predictions[0])
        
        predicted_label = CLASS_LABELS.get(predicted_index, "Невідомий звук")
        confidence = np.max(predictions[0])
        
        # 4. Повернення результату
        return (
            f"ANALYSIS.OUTPUT: CLASSIFIED AS '{predicted_label}' "
            f"(Confidence: {confidence:.2f}). "
            f"Vector Size: {mfcc_input.shape[1]}"
        )
        
    except Exception as e:
        return f"ANALYSIS.OUTPUT: CRITICAL.ERROR: Prediction failed. Details: {str(e)}"
    
_yamnet_model = None
_class_names = None

def get_yamnet():
    global _yamnet_model, _class_names

    if _yamnet_model is None:
        print("--- [AI INIT] Loading YAMNet from TensorFlow Hub ---")
        _yamnet_model = hub.load("https://tfhub.dev/google/yamnet/1")

        # Завантажуємо назви класів
        class_map_path = os.path.join(settings.BASE_DIR, "machine_era/models/yamnet_class_map.csv")
        with open(class_map_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            _class_names = [row["display_name"] for row in reader]

    return _yamnet_model, _class_names


def load_audio_for_yamnet(audio_path):
    audio = AudioSegment.from_file(audio_path)

    # YAMNet ВИМАГАЄ: mono, 16kHz
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)

    samples = np.array(audio.get_array_of_samples()).astype(np.float32)

    # нормалізація [-1, 1]
    samples /= np.iinfo(audio.array_type).max
    return samples


def analyze_audio(audio_path):
    if not os.path.exists(audio_path):
        return "ERROR: Audio file not found."

    model, class_names = get_yamnet()
    if model is None:
        return "ERROR: YAMNet not loaded."

    try:
        waveform = load_audio_for_yamnet(audio_path)

        # YAMNet output
        scores, embeddings, spectrogram = model(waveform)

        # Середній score по часу
        mean_scores = tf.reduce_mean(scores, axis=0).numpy()

        top_index = np.argmax(mean_scores)
        label = class_names[top_index]
        confidence = mean_scores[top_index]

        return (
            f"ANALYSIS.OUTPUT: CLASSIFIED AS '{label}' "
            f"(Confidence: {confidence:.2f})"
        )

    except Exception as e:
        return f"CRITICAL.ERROR: {str(e)}"