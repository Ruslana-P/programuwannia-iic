# djangotutorial/image_classifier/ai_model.py

import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
from PIL import Image
import os
import json

# --- Визначення шляхів до локальних файлів ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 1. Шлях до файлу ваг (один рівень вище, у djangotutorial/)
WEIGHTS_FILENAME = 'vgg16_weights_tf_dim_ordering_tf_kernels.h5'
LOCAL_WEIGHTS_PATH = os.path.join(BASE_DIR, '..', WEIGHTS_FILENAME)
# 2. Шлях до файлу індексів класів (у поточній папці machine_era/)
INDEX_PATH = os.path.join(BASE_DIR, 'imagenet_class_index.json')

# --- Завантаження моделі (виконується лише один раз) ---
MODEL = None
CLASS_INDEX = None

try:
    if os.path.exists(LOCAL_WEIGHTS_PATH):
        # Завантажуємо модель, використовуючи локально завантажені ваги
        MODEL = VGG16(weights=LOCAL_WEIGHTS_PATH)
        print("Модель VGG16 успішно завантажена локально.")
    else:
        print(f"Помилка: Файл ваг '{WEIGHTS_FILENAME}' не знайдено за шляхом: {LOCAL_WEIGHTS_PATH}")
except Exception as e:
    print(f"Помилка ініціалізації моделі VGG16: {e}")
    
# --- Функція декодування (використовує локальний файл індексів) ---

def decode_predictions_local(preds, top=5):
    """
    Завантажує індекс класів локально та декодує прогнози.
    """
    global CLASS_INDEX

    if CLASS_INDEX is None:
        if os.path.exists(INDEX_PATH):
            try:
                # Завантажуємо файл індексів класів з локального диска
                with open(INDEX_PATH) as f:
                    CLASS_INDEX = json.load(f)
            except Exception as e:
                print(f"Помилка завантаження локального JSON-індексу: {e}")
                return [[]] * len(preds)
        else:
            # Якщо індекс не знайдено, ми не можемо декодувати.
            print(f"Помилка: Файл індексів '{os.path.basename(INDEX_PATH)}' не знайдено.")
            return [[]] * len(preds)

    results = []
    for pred in preds:
        # Отримуємо індекси топ-класів
        top_indices = pred.argsort()[-top:][::-1] 
        # Зіставляємо індекси з назвами класів
        result = [tuple(CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
        results.append(result)
    return results


# --- Основна функція класифікації, яка викликатиметься у Django ---

def classify_image(image_path):
    """
    Завантажує зображення, обробляє його та класифікує.
    """
    if not MODEL:
        return "Помилка: Модель AI не завантажена."
        
    try:
        # 1. Завантаження та зміна розміру
        img = Image.open(image_path)
        img = img.resize((224, 224))
        
        img_array = keras_image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) 
        
        # 2. Попередня обробка та прогнозування
        img_array = preprocess_input(img_array)
        predictions = MODEL.predict(img_array, verbose=0)
        
        # 3. Декодування результатів (використовуємо локальну функцію)
        decoded_predictions = decode_predictions_local(predictions, top=3)[0] 

        # 4. Форматування результату для виводу
        results = [
            f"{label}: {score*100:.2f}%" 
            for (_, label, score) in decoded_predictions
        ]
        return " | ".join(results)
        
    except Exception as e:
        return f"Помилка при класифікації: {e}"