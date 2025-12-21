import io
from typing import Dict, List

import numpy as np
from pydub import AudioSegment


def _load_mono_signal(path: str, target_rate: int = 16000) -> np.ndarray:
    """
    Завантажує аудіофайл у моно формат з фіксованою частотою дискретизації.
    Повертає numpy-масив сигналу в діапазоні [-1, 1].
    """
    audio: AudioSegment = AudioSegment.from_file(path)
    audio = audio.set_channels(1).set_frame_rate(target_rate)

    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    max_abs = np.max(np.abs(samples)) or 1.0
    samples = samples / max_abs
    return samples


def analyze_signal_spectrum(path: str, top_k: int = 5) -> Dict[str, object]:
    """
    Обчислює модуль спектру сигналу й повертає коротке резюме:
    - домінуючі частоти
    - тип спектра (низько/середньо/високочастотний, шумовий тощо).
    """
    signal = _load_mono_signal(path)
    n = len(signal)

    # Вікно Хеннінга для зменшення витікань спектру
    window = np.hanning(n)
    spectrum = np.fft.rfft(signal * window)
    freqs = np.fft.rfftfreq(n, d=1.0 / 16000)

    magnitudes = np.abs(spectrum)
    if magnitudes.size == 0:
        return {"dominant_frequencies": [], "summary": "Signal is empty or corrupted."}

    # Топ-K піків (пропускаємо нульову частоту)
    peak_indices: np.ndarray = np.argsort(magnitudes[1:])[-top_k:] + 1
    peak_indices = peak_indices[::-1]

    dominant: List[Dict[str, float]] = []
    total_energy = float(np.sum(magnitudes**2)) or 1.0

    for idx in peak_indices:
        freq_hz = float(freqs[idx])
        rel_energy = float((magnitudes[idx] ** 2) / total_energy)
        dominant.append(
            {
                "frequency_hz": round(freq_hz, 1),
                "relative_energy": round(rel_energy * 100.0, 3),  # у відсотках
            }
        )

    # Просте "класифікування" типу спектра
    mean_freq = np.average(freqs, weights=magnitudes)
    if mean_freq < 500:
        spectrum_type = "LOW-FREQUENCY / HUM-LIKE SIGNAL"
    elif mean_freq < 3000:
        spectrum_type = "MID-BAND / SPEECH-LIKE SIGNAL"
    else:
        spectrum_type = "HIGH-FREQUENCY / NOISY SIGNAL"

    summary = (
        f"SPECTRUM.TYPE: {spectrum_type}. "
        f"DOMINANT.FREQS: "
        + ", ".join(f"{p['frequency_hz']}Hz ({p['relative_energy']}%)" for p in dominant)
    )

    return {
        "dominant_frequencies": dominant,
        "summary": summary,
    }