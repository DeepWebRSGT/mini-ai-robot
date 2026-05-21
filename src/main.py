"""
Mini AI Robot — Ana Döngü
==========================
Tüm bileşenleri birleştiren ana program.
Çalıştır: python main.py
"""

import logging
import signal
import sys
import time
from pathlib import Path

# Proje kökünü PYTHONPATH'e ekle
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    LLM, CORAL, BEHAVIOR, GPIO_PINS, LANGUAGES
)


class MiniAIRobot:
    """Ana robot sınıfı — tüm bileşenleri yönetir"""

    def __init__(self):
        self.running = True
        self.mode = "intent"  # "intent" veya "llm"
        self.components = {}
        self._setup_logging()
        self._init_components()
        self._setup_signal_handlers()

    def _setup_logging(self):
        """Loglama ayarları"""
        level = logging.DEBUG if BEHAVIOR["debug"] else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )
        self.log = logging.getLogger("Robot")

    def _init_components(self):
        """Tüm bileşenleri başlat"""
        self.log.info("=" * 40)
        self.log.info("🤖 Mini AI Robot başlatılıyor...")
        self.log.info("=" * 40)

        # 1. Buton
        try:
            from button import ButtonController, LEDController
            self.components["button"] = ButtonController(
                callback=self._on_button_press
            )
            self.components["led"] = LEDController()
            self.log.info("✅ Buton ve LED hazır")
        except Exception as e:
            self.log.warning(f"Buton başlatılamadı: {e}")

        # 2. Ekran
        try:
            from display import RobotFace
            self.components["display"] = RobotFace()
            self.components["display"].show_splash()
            self.components["display"].show_face("neutral", "Hallo!")
            self.log.info("✅ Ekran hazır")
        except Exception as e:
            self.log.warning(f"Ekran başlatılamadı: {e}")

        # 3. STT (Ses Tanıma)
        try:
            from stt import SpeechRecognizer
            self.components["stt"] = SpeechRecognizer()
            self.log.info("✅ STT (Vosk) hazır")
        except Exception as e:
            self.log.warning(f"STT başlatılamadı: {e}")

        # 4. TTS (Ses Sentezi)
        try:
            from tts import TextToSpeech
            self.components["tts"] = TextToSpeech()
            self.log.info("✅ TTS (Piper) hazır")
        except Exception as e:
            self.log.warning(f"TTS başlatılamadı: {e}")

        # 5. Intent Classifier
        try:
            from intent import IntentClassifier, IntentResponder
            self.components["intent_classifier"] = IntentClassifier()
            self.components["intent_responder"] = IntentResponder(
                language=BEHAVIOR["language"]
            )
            self.log.info("✅ Intent sınıflandırıcı hazır")
        except Exception as e:
            self.log.warning(f"Intent sistemi başlatılamadı: {e}")

        # 6. LLM (Opsiyonel — 4GB Pi'de)
        if LLM["enabled"]:
            try:
                from llm import LocalLLM
                self.components["llm"] = LocalLLM()
                if self.components["llm"].available:
                    self.mode = "llm"
                    self.log.info("✅ LLM hazır — akıllı mod aktif!")
                else:
                    self.log.info("ℹ️  LLM kullanılamıyor, intent moduna geçiliyor")
                    self.mode = "intent"
            except Exception as e:
                self.log.warning(f"LLM başlatılamadı: {e}")

        # 7. Kamera (Opsiyonel)
        if CORAL["enabled"]:
            try:
                from camera import CameraVision
                self.components["camera"] = CameraVision()
                if self.components["camera"].cap:
                    self.log.info("✅ Kamera hazır")
            except Exception as e:
                self.log.warning(f"Kamera başlatılamadı: {e}")

        # Bileşen özeti
        loaded = [k for k, v in self.components.items() if v]
        self.log.info(f"📦 Yüklenen bileşenler: {', '.join(loaded)}")
        self.log.info(f"🎯 Çalışma modu: {self.mode.upper()}")
        self.log.info("🤖 Robot hazır! Butona bas ve konuş.\n")

    def _setup_signal_handlers(self):
        """Ctrl+C vs. için sinyal yakalayıcılar"""
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

    def _handle_signal(self, signum, frame):
        """Sinyal alındığında güvenli kapanış"""
        self.log.info("\n🛑 Kapatılıyor...")
        self.running = False

    def _on_button_press(self):
        """Butona basılınca tetiklenir"""
        self.log.info("🔘 Buton algılandı!")
        self._process_conversation()

    def _set_expression(self, expression, text=""):
        """Robot yüz ifadesini güncelle"""
        display = self.components.get("display")
        if display:
            display.show_face(expression, text)

    def _speak(self, text):
        """Sesli yanıt ver"""
        if not text:
            return

        tts = self.components.get("tts")
        display = self.components.get("display")

        if display:
            display.show_face("thinking", text)

        if tts:
            tts.speak(text)

        # Ekranda göster
        if display:
            display.show_face("happy", text)

    def _listen(self):
        """Kullanıcının sesini dinle ve metne çevir"""
        stt = self.components.get("stt")
        if not stt:
            return ""

        display = self.components.get("display")
        led = self.components.get("led")

        if display:
            display.show_face("thinking", "Luisteren...")

        if led:
            led.on()

        self.log.info("🎤 Dinliyorum...")
        text = stt.listen(timeout=BEHAVIOR["wake_timeout"])

        if led:
            led.off()

        if text:
            self.log.info(f"🗣️  Kullanıcı: {text}")
        else:
            self.log.info("🔇 Ses algılanmadı")

        return text

    def _process_conversation(self):
        """Bir konuşma turunu işle"""
        
        # 1. Kullanıcıyı dinle
        user_text = self._listen()
        if not user_text:
            self._set_expression("neutral", "Ik hoorde niets...")
            return

        # 2. Yanıt üret
        response = self._generate_response(user_text)

        # 3. Sesli yanıt ver
        if response:
            self._speak(response)
        else:
            self._speak("Sorry, ik kon geen antwoord bedenken.")

    def _generate_response(self, user_text):
        """Kullanıcı metnine yanıt üret
        
        3 kanal:
          A) Coral + Intent → hızlı kural tabanlı (her zaman)
          B) LLM → akıllı yanıt (4GB Pi'de)
          C) Hibrit → intent'e göre LLM veya kural
        """
        # Önce intent'i belirle
        classifier = self.components.get("intent_classifier")
        responder = self.components.get("intent_responder")

        if classifier and responder:
            intent = classifier.classify(user_text)
            self.log.info(f"🎯 Intent: {intent}")

            # Bilinen intent → hemen yanıt
            if intent != "unknown":
                return responder.respond(intent)

        # Bilinmeyen intent → LLM dene
        llm = self.components.get("llm")
        if llm and llm.available:
            self.log.info("🧠 LLM çağrılıyor...")
            self._set_expression("thinking", "Denken...")

            response = llm.ask(user_text)
            if response:
                return response

        # LLM yoksa veya yanıt alamazsan → generic yanıt
        if responder:
            return responder.respond("unknown")

        return ""

    def run(self):
        """Ana döngüyü başlat"""
        self.log.info("🤖 Mini AI Robot çalışıyor!")
        self.log.info("  Butona bas → konuş → robot cevaplar")
        self.log.info("  Ctrl+C ile çıkış\n")

        # Hoş geldin mesajı
        self._speak("Hallo! Ik ben Mini AI Robot. Druk op de knop en praat met me!")

        # Ana döngü: buton bekler, buton gelince konuşma başlar
        while self.running:
            try:
                button = self.components.get("button")
                if button:
                    # Buton bekleme modunda bekle
                    button.wait_for_press(timeout=1)
                else:
                    # Buton yoksa her 5 saniyede bir kontrol et
                    time.sleep(5)
                    self._process_conversation()
                
                time.sleep(0.1)

            except KeyboardInterrupt:
                break
            except Exception as e:
                self.log.error(f"Döngü hatası: {e}")
                time.sleep(2)

        self.cleanup()

    def cleanup(self):
        """Kaynakları temizle"""
        self.log.info("🧹 Temizleniyor...")
        
        self._set_expression("sleep", "Tot ziens...")
        
        for name, component in self.components.items():
            if component and hasattr(component, "cleanup"):
                try:
                    component.cleanup()
                except Exception as e:
                    self.log.debug(f"Temizlik ({name}): {e}")

        self.log.info("👋 Robot kapandı. Görüşürüz!")


if __name__ == "__main__":
    robot = MiniAIRobot()
    robot.run()
