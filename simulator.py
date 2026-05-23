#!/usr/bin/env python3
"""
Mini AI Robot — Terminal Simulator
====================================
Donanım olmadan robot AI'sini test etmek için terminal emülatörü.
Tüm AI mantığı (intent classifier, yanıt üretimi) aynen korunur.
Sadece giriş/çıkış kanalları taklit edilir.

Kullanım:  python simulator.py
"""

import sys
import time
import random
import threading
from pathlib import Path
from datetime import datetime

# Proje src'ini ekle
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import BEHAVIOR, LANGUAGES


# =============================================
# TERMİNAL EKRAN EMÜLATÖRÜ
# =============================================
class TerminalFace:
    """TFT ekran yerine terminalde ASCII yüz gösterimi"""

    FACES = {
        "neutral": """
    ╭─────────╮
    │  ●   ●  │
    │    ⎯    │
    │  ─────  │
    ╰─────────╯
""",
        "happy": """
    ╭─────────╮
    │  ◕‿◕  │
    │         │
    │  ╰▰╯  │
    ╰─────────╯
""",
        "sad": """
    ╭─────────╮
    │  ◕‿◕  │
    │         │
    │  ╰╮╯  │
    ╰─────────╯
""",
        "surprised": """
    ╭─────────╮
    │  ○   ○  │
    │    ○    │
    │   ○○○   │
    ╰─────────╯
""",
        "thinking": """
    ╭─────────╮
    │  ◔   ◔  │
    │    ╭╮   │
    │  ╰──╯  │
    ╰─────────╯
""",
        "sleep": """
    ╭─────────╮
    │  ─   ─  │
    │         │
    │  ─────  │
    ╰─────────╯
""",
        "love": """
    ╭─────────╮
    │  ♥   ♥  │
    │    ⎯    │
    │  ─────  │
    ╰─────────╯
""",
        "angry": """
    ╭─────────╮
    │  >   <  │
    │    ⎯    │
    │  ─────  │
    ╰─────────╯
""",
    }

    def __init__(self):
        self.expression = "neutral"
        self._clear()

    def _clear(self):
        """Terminali temizle"""
        print("\033[2J\033[H", end="")

    def show_splash(self):
        self._clear()
        logo = """
    ╔═══════════════════════╗
    ║                       ║
    ║   🤖 Mini AI Robot   ║
    ║                       ║
    ║   [SİMÜLASYON MODU]  ║
    ║                       ║
    ╚═══════════════════════╝
"""
        print(logo)
        time.sleep(1.5)

    def show_face(self, expression="neutral", text=""):
        self.expression = expression
        self._clear()
        face = self.FACES.get(expression, self.FACES["neutral"])
        emoji_map = {
            "neutral": "🤖", "happy": "😊", "sad": "😢",
            "surprised": "😮", "thinking": "🤔", "sleep": "😴",
            "love": "🥰", "angry": "😠",
        }
        emoji = emoji_map.get(expression, "🤖")
        print(f"\n  {emoji}  {expression.upper()}")
        print(face)
        if text:
            # Metni 40 karaktere sar
            words = text.split()
            lines = []
            current = ""
            for word in words:
                if len(current + " " + word) > 40:
                    lines.append(current)
                    current = word
                else:
                    current = f"{current} {word}".strip()
            if current:
                lines.append(current)
            print(f"  {'─' * 42}")
            for line in lines[:4]:
                print(f"  {line}")
            print(f"  {'─' * 42}")
        print()

    def show_volume(self, level):
        bar_len = 20
        filled = int(bar_len * level)
        bar = "█" * filled + "░" * (bar_len - filled)
        sys.stdout.write(f"\r  Ses: |{bar}| {int(level*100)}%")
        sys.stdout.flush()

    def clear(self):
        self._clear()


# =============================================
# TERMİNAL STT EMÜLATÖRÜ (klavye girişi)
# =============================================
class TerminalSTT:
    """Vosk yerine klavyeden metin al"""

    def __init__(self):
        self.running = False

    def listen(self, timeout=5):
        """Kullanıcıdan metin al (enter ile bitir)"""
        print(f"  🎤 Dinliyorum (yaz ve Enter'a bas, süre: {timeout}s)...")
        print("  > ", end="", flush=True)
        try:
            text = sys.stdin.readline().strip()
            return text
        except (KeyboardInterrupt, EOFError):
            return ""

    def listen_one_shot(self, button_pin=None):
        """Push-to-talk simülasyonu"""
        print("  [Butona basıldı!]")
        return self.listen()

    def start_microphone(self):
        self.running = True

    def stop(self):
        self.running = False


# =============================================
# TERMİNAL TTS EMÜLATÖRÜ (ekrana yaz)
# =============================================
class TerminalTTS:
    """Piper yerine metni terminalde göster"""

    def speak(self, text):
        if not text:
            return
        print(f"  🔊 Robot: {text}")
        time.sleep(0.3)

    def speak_async(self, text, callback=None):
        self.speak(text)
        if callback:
            callback()


# =============================================
# TERMİNAL BUTON EMÜLATÖRÜ
# =============================================
class TerminalButton:
    """GPIO buton yerine Enter tuşu"""

    def __init__(self, pin=None, callback=None):
        self.callback = callback
        self._running = False

    def wait_for_press(self, timeout=None):
        """Enter tuşunu bekle"""
        print("\n  [🔘 Robot hazır! Konuşmak için Enter'a bas / Ctrl+C çıkış]")
        try:
            sys.stdin.readline()
            if self.callback:
                self.callback()
            return True
        except KeyboardInterrupt:
            return False

    def cleanup(self):
        pass


class TerminalLED:
    """Durum LED'i simülasyonu"""

    def on(self):
        print("  💡 [LED: AÇIK]")

    def off(self):
        print("  💡 [LED: KAPALI]")

    def blink(self, count=3, interval=0.3):
        for _ in range(count):
            print(f"  💡 [LED: YANIP SÖNÜYOR]")
            time.sleep(interval)

    def cleanup(self):
        self.off()


# =============================================
# ROBOT ÇEKİRDEĞİ (gerçek AI mantığı)
# =============================================
from intent import IntentClassifier, IntentResponder


class MiniRobotSimulator:
    """Ana robot sınıfı — donanımsız çalışır"""

    def __init__(self, language="tr"):
        self.running = True
        self.mode = "intent"
        self.language = language

        print("╔══════════════════════════════════════╗")
        print("║   🤖 MINI AI ROBOT — SİMÜLASYON     ║")
        print("║                                      ║")
        print(f"║   Dil: {language.upper():>27s}║")
        print("║   Mod: Intent-Based (çevrimdışı AI) ║")
        print("║   Donanım: TAKLİT (tüm AI gerçek)   ║")
        print("╚══════════════════════════════════════╝")

        # Bileşenler (terminal emülasyonu)
        self.display = TerminalFace()
        self.stt = TerminalSTT()
        self.tts = TerminalTTS()
        self.button = TerminalButton(callback=self._on_button_press)
        self.led = TerminalLED()

        # Gerçek AI (IntentClassifier aynen kullanılır)
        self.classifier = IntentClassifier()
        self.responder = IntentResponder(language=language)

        self.display.show_splash()

    def _on_button_press(self):
        """Butona basılınca — konuşma başlat"""
        self._process_conversation()

    def _set_expression(self, expr, text=""):
        self.display.show_face(expr, text)

    def _speak(self, text):
        if not text:
            return
        self._set_expression("thinking", text)
        self.tts.speak(text)
        self._set_expression("happy", text)

    def _listen(self):
        self._set_expression("thinking", "Dinliyorum...")
        self.led.on()
        text = self.stt.listen(timeout=60)
        self.led.off()

        if text:
            print(f"  🗣️  Kullanıcı: {text}")
        else:
            print("  🔇 Ses/Klavye algılanmadı")
        return text

    def _process_conversation(self):
        user_text = self._listen()
        if not user_text:
            self._set_expression("neutral", "Bir şey duymadım...")
            return

        response = self._generate_response(user_text)
        if response:
            self._speak(response)
        else:
            self._speak("Anlamadım, tekrar eder misin? 🤔")

    def _generate_response(self, user_text):
        # Intent sınıflandır (GERÇEK AI — intent.py aynen kullanılır)
        intent = self.classifier.classify(user_text)
        print(f"  🎯 Intent: {intent}")
        self._set_expression("thinking", f"Intent: {intent}")

        if intent != "unknown":
            return self.responder.respond(intent)

        # unknown → Ollama'ya dene (varsa)
        try:
            from llm import LocalLLM
            llm = LocalLLM()
            if llm.available:
                print("  🧠 LLM çağrılıyor (Ollama)...")
                response = llm.ask(user_text)
                if response:
                    return response
        except Exception as e:
            print(f"  ⚠️  LLM kullanılamıyor: {e}")

        return self.responder.respond("unknown")

    def run(self):
        """Ana döngü"""
        self._speak("Merhaba! Ben Mini AI Robot! Konuşmak için Enter'a bas!")
        print()
        print("  ──────────────────────────────────────")
        print("  🤖 ROBOT HAZIR! Test komutları:")
        print("     ✨ Herhangi bir şey yaz ve Enter bas")
        print("     ✨ Çıkmak için Ctrl+C")
        print("  ──────────────────────────────────────")

        while self.running:
            try:
                self.button.wait_for_press(timeout=1)
            except KeyboardInterrupt:
                print("\n  👋 Görüşürüz!")
                break

        self.cleanup()

    def cleanup(self):
        self._set_expression("sleep", "Görüşürüz...")
        print("\n  🧹 Simülasyon kapatılıyor...")
        self.button.cleanup()
        self.led.cleanup()
        print("  ✅ Simülasyon sonlandı.")


# =============================================
# TOPLU TEST (otomatik, kullanıcı girişi yok)
# =============================================
def run_auto_test():
    """Tüm AI mantığını otomatik test et (kullanıcı girişi gerekmez)"""
    print("\n" + "=" * 55)
    print("  🤖 MINI AI ROBOT — OTOMATİK TEST")
    print("  (Donanım yok, AI çekirdeği gerçek)")
    print("=" * 55)

    # 1. IntentClassifier testi
    print("\n  [1/4] IntentClassifier yükleniyor...")
    classifier = IntentClassifier()
    responder = IntentResponder(language="tr")
    print("  ✅ IntentClassifier hazır")

    # 2. Intent tanıma testleri
    print("\n  [2/4] Intent tanıma testleri")
    test_cases = [
        # (metin, beklenen_intent)
        ("Merhaba", "greeting"),
        ("Selam", "greeting"),
        ("Saat kaç", "time"),
        ("Bugün günlerden ne", "date"),
        ("Tarih nedir", "date"),
        ("Hava nasıl", "weather"),
        ("Yağmur yağıyor mu", "weather"),
        ("Adın ne", "name"),
        ("Sen kimsin", "name"),
        ("Nasılsın", "how_are_you"),
        ("İyi misin", "how_are_you"),
        ("Şaka yap", "joke"),
        ("Fıkra anlat", "joke"),
        ("Şarkı söyle", "music"),
        ("Müzik çal", "music"),
        ("Görüşürüz", "goodbye"),
        ("Hoşçakal", "goodbye"),
        ("Hallo", "greeting"),
        ("Hoe laat", "time"),
        ("Doei", "goodbye"),
        ("Android telefon nasıl yapılır", "unknown"),
        ("Python öğrenmek istiyorum", "unknown"),
    ]

    passed = 0
    failed = 0
    for text, expected in test_cases:
        intent = classifier.classify(text)
        status = "✅" if intent == expected else "❌"
        if intent == expected:
            passed += 1
        else:
            failed += 1
        print(f"    {status} '{text}' → {intent} (beklenen: {expected})")

    print(f"\n    Sonuç: {passed}/{len(test_cases)} başarılı, {failed} başarısız")

    # 3. Yanıt üretimi testi
    print("\n  [3/4] Yanıt üretimi testleri")
    for intent in ["greeting", "time", "date", "weather", "name",
                    "how_are_you", "joke", "music", "goodbye", "unknown"]:
        response = responder.respond(intent)
        print(f"    {intent:15s} → '{response}'")

    # 4. Türkçe-Hollandaca çift dil testi
    print("\n  [4/4] Çoklu dil testi")
    for lang in ["tr", "nl"]:
        r = IntentResponder(language=lang)
        resp = r.respond("greeting")
        print(f"    Dil={lang}: '{resp}'")

    print("\n" + "=" * 55)
    print(f"  ✅ OTOMATİK TEST TAMAMLANDI — {passed}/{len(test_cases)} intent doğru")
    print("=" * 55)


if __name__ == "__main__":
    import sys

    if "--test" in sys.argv or "-t" in sys.argv:
        run_auto_test()
    elif "--interactive" in sys.argv or "-i" in sys.argv:
        robot = MiniRobotSimulator(language="tr")
        robot.run()
    else:
        # Varsayılan: önce otomatik test, sonra interaktif
        run_auto_test()
        print("\n  ──────────────────────────────────────")
        print("  🤖 İnteraktif moda geçiliyor...")
        print("  ──────────────────────────────────────\n")
        robot = MiniRobotSimulator(language="tr")
        robot.run()
