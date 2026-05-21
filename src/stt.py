"""
STT (Speech-to-Text) — Vosk ile Offline Ses Tanıma
=====================================================
INMP441 I2S mikrofonundan ses alır, Vosk ile metne çevirir.
"""

import json
import queue
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import pyaudio
    from vosk import Model, KaldiRecognizer
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    logger.warning("Vosk veya PyAudio kurulu değil. 'pip install vosk pyaudio'")

from config import STT


class SpeechRecognizer:
    """Vosk tabanlı offline ses tanıma"""

    def __init__(self, model_path=None, sample_rate=None):
        self.model_path = model_path or STT["model_path"]
        self.sample_rate = sample_rate or STT["sample_rate"]
        self.audio_queue = queue.Queue()
        self.recognizer = None
        self.audio = None
        self.stream = None
        self._setup()

    def _setup(self):
        """Vosk modelini yükle"""
        if not VOSK_AVAILABLE:
            raise RuntimeError("Vosk kurulu değil. Çalıştır: pip install vosk pyaudio")

        model_dir = Path(self.model_path)
        if not model_dir.exists():
            raise FileNotFoundError(
                f"Vosk modeli bulunamadı: {model_dir}\n"
                f"İndirmek için: models/download_models.sh çalıştır"
            )

        logger.info(f"Vosk modeli yükleniyor: {model_dir}")
        self.model = Model(str(model_dir))
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
        self.recognizer.SetWords(False)
        logger.info("Vosk hazır!")

    def start_microphone(self):
        """Mikrofon akışını başlat"""
        self.audio = pyaudio.PyAudio()

        # INMP441 I2S mikrofonu için
        # ALSA üzerinden I2S cihazını bul
        device_index = None
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            logger.debug(f"Ses cihazı [{i}]: {info['name']}")
            if "I2S" in info["name"] or "googlevoicehat" in info["name"]:
                device_index = i
                break

        if device_index is None:
            # Varsayılan cihazı kullan
            logger.info("I2S cihazı bulunamadı, varsayılan kullanılıyor")
            device_index = self.audio.get_default_input_device_info()["index"]

        logger.info(f"Mikrofon başlatılıyor: cihaz [{device_index}]")
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=4000,
            stream_callback=self._audio_callback,
        )
        self.stream.start_stream()

    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Ses verisi geldiğinde kuyruğa ekle"""
        self.audio_queue.put(in_data)
        return (None, pyaudio.paContinue)

    def listen(self, timeout=5):
        """Bir kere dinle ve metne çevir
        
        Returns:
            str: Tanınan metin (boş olabilir)
        """
        import time
        start = time.time()
        full_text = []

        while time.time() - start < timeout:
            try:
                data = self.audio_queue.get(timeout=0.5)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        full_text.append(text)
            except queue.Empty:
                # Ses yok, devam et
                if full_text:  # Konuşma bitti mi?
                    break
                continue

        # Kalan kısmı da al
        result = json.loads(self.recognizer.FinalResult())
        text = result.get("text", "").strip()
        if text:
            full_text.append(text)

        return " ".join(full_text)

    def listen_one_shot(self, button_pin=None):
        """Butonla tetiklenen tek seferlik dinleme
        
        GPIO butonu bekler, basılınca dinlemeye başlar, 
        sessizlik algılayınca durur.
        
        Returns:
            str: Tanınan metin
        """
        if button_pin:
            import RPi.GPIO as GPIO
            logger.info("Butona bas ve konuş...")
            GPIO.wait_for_edge(button_pin, GPIO.FALLING)

        self.start_microphone()
        text = self.listen(timeout=STT["timeout"])
        self.stop()
        return text

    def stop(self):
        """Mikrofonu durdur"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()

    def __del__(self):
        self.stop()


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    print("🎤 STT Test — Konuşmaya başla (Ctrl+C çıkış)")
    
    recognizer = SpeechRecognizer()
    recognizer.start_microphone()
    
    try:
        while True:
            text = recognizer.listen(timeout=3)
            if text:
                print(f"  → {text}")
    except KeyboardInterrupt:
        recognizer.stop()
        print("\nGörüşürüz!")
