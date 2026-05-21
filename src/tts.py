"""
TTS (Text-to-Speech) — Piper ile Offline Ses Sentezi
=======================================================
MAX98357A I2S amplifikatör + mini speaker'a ses çıkışı.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import piper_tts
    import sounddevice as sd
    import numpy as np
    PIPER_AVAILABLE = True
except ImportError:
    PIPER_AVAILABLE = False
    logger.warning("Piper TTS kurulu değil. 'pip install piper-tts sounddevice numpy'")

from config import TTS


class TextToSpeech:
    """Piper ile offline ses sentezi"""

    def __init__(self, model_path=None, config_path=None, sample_rate=None):
        self.model_path = model_path or TTS["model_path"]
        self.config_path = config_path or TTS["config_path"]
        self.sample_rate = sample_rate or TTS["sample_rate"]
        self.pipe = None
        self._setup()

    def _setup(self):
        """Piper modelini yükle"""
        if not PIPER_AVAILABLE:
            raise RuntimeError(
                "Piper TTS kurulu değil.\n"
                "Çalıştır: pip install piper-tts sounddevice numpy"
            )

        model_file = Path(self.model_path)
        if not model_file.exists():
            raise FileNotFoundError(
                f"Piper ses modeli bulunamadı: {model_file}\n"
                f"İndirmek için: models/download_models.sh çalıştır"
            )

        logger.info(f"Piper modeli yükleniyor: {model_file}")
        self.pipe = piper_tts.PiperVoice(self.model_path, config_path=self.config_path)
        logger.info("Piper TTS hazır!")

    def speak(self, text):
        """Metni sese çevir ve çal
        
        Args:
            text: Söylenecek metin
        """
        if not text:
            return

        logger.info(f"🔊 Söyleniyor: {text}")

        try:
            # Ses sentezi
            audio_stream = self.pipe.synthesize(text)
            audio_data = b"".join(audio_stream)
            
            # Ses seviyesini ayarla
            samples = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
            samples *= TTS.get("speed", 1.0)
            samples = np.clip(samples, -32768, 32767).astype(np.int16)

            # I2S üzerinden çal (MAX98357A)
            sd.play(samples, samplerate=self.sample_rate)
            sd.wait()

        except Exception as e:
            logger.error(f"Ses çalma hatası: {e}")
            # Fallback: eSpeakNG
            self._fallback_speak(text)

    def _fallback_speak(self, text):
        """eSpeakNG ile yedek ses çıkışı (Piper çalışmazsa)"""
        import subprocess
        try:
            subprocess.run(
                ["espeak-ng", "-v", "nl", "-s", "130", text],
                timeout=10
            )
        except Exception as e:
            logger.error(f"eSpeakNG hatası: {e}")

    def speak_async(self, text, callback=None):
        """Arka planda ses çal (bloklamaz)"""
        import threading
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.daemon = True
        thread.start()
        if callback:
            thread.join()
            callback()


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    print("🔊 TTS Test — Çalıştırılıyor...")
    
    tts = TextToSpeech()
    tts.speak("Hallo! Ik ben Mini AI Robot. Leuk je te ontmoeten!")
    print("✅ Test tamamlandı")
