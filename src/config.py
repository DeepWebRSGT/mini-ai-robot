"""
mini-ai-robot — Merkezi Yapılandırma
======================================
Tüm ayarlar tek bir yerden yönetilir.
"""

import os
from pathlib import Path

# === Proje Yolu ===
PROJECT_DIR = Path(__file__).parent.parent
MODELS_DIR = PROJECT_DIR / "models"

# === STT (Vosk) ===
STT = {
    "model_path": str(MODELS_DIR / "vosk-model-small-nl-0.22"),
    "sample_rate": 16000,
    "language": "nl",  # nl, tr, en, fr, de
    "timeout": 5,       # saniye
}

# === TTS (Piper) ===
TTS = {
    "model_path": str(MODELS_DIR / "nl_NL-glow-tts-medium.onnx"),
    "config_path": str(MODELS_DIR / "nl_NL-glow-tts-medium.onnx.json"),
    "sample_rate": 22050,
    "speed": 1.0,
}

# === LLM (Ollama) ===
LLM = {
    "enabled": True,        # False = sadece intent-based
    "model": "qwen2.5:0.5b",
    "host": "http://localhost:11434",
    "timeout": 30,
    "system_prompt": (
        "Sen sevimli bir masaüstü robot asistanısın. "
        "Adı 'Mini AI Robot'. Kısa, tatlı ve arkadaşça cevaplar ver. "
        "Maksimum 2 cümle. Kullanıcıyla Hollandaca konuş."
    ),
}

# === Coral TPU ===
CORAL = {
    "enabled": False,       # Coral USB takılı mı?
    "intent_model": str(MODELS_DIR / "intent_model_edgetpu.tflite"),
    "embedding_model": str(MODELS_DIR / "embedding_model_edgetpu.tflite"),
}

# === Ekran (ILI9341 TFT) ===
DISPLAY = {
    "width": 240,
    "height": 320,
    "spi_frequency": 32000000,
    "cs_pin": 8,      # GPIO8 (CE0)
    "dc_pin": 25,     # GPIO25
    "rst_pin": 24,    # GPIO24
    "backlight_pin": 18,  # GPIO18 (PWM)
}

# === GPIO Pinleri ===
GPIO_PINS = {
    "button": 17,       # Bas-konuş butonu
    "led_status": 22,   # Durum LED'i
    "i2s_bclk": 18,     # I2S bit clock (PWM0)
    "i2s_wclk": 19,     # I2S word clock
    "i2s_dout": 21,     # I2S data out (MAX98357A)
    "i2s_din": 20,      # I2S data in (INMP441)
}

# === Davranış ===
BEHAVIOR = {
    "wake_timeout": 60,       # sn — hareketsizlikte bekleme
    "volume": 0.8,            # 0.0 - 1.0
    "language": "nl",         # nl, tr, en
    "debug": True,            # Konsola detaylı log
}

# === Önceden Tanımlı Yanıtlar (Intent-Based Mod) ===
INTENT_RESPONSES_NL = {
    "greeting": [
        "Hallo! Ik ben Mini AI Robot! 🐱",
        "Hoi! Hoe gaat het?",
        "Hey! Leuk je te zien!",
    ],
    "time": ["Het is nu {time}"],
    "date": ["Vandaag is het {date}"],
    "weather": [
        "Ik heb geen internet, maar het ziet er mooi uit!",
        "Geen idee, ik ben offline! Maar hopelijk schijnt de zon ☀️",
    ],
    "name": [
        "Ik heet Mini AI Robot! Aangenaam!",
        "Mini AI Robot, dat ben ik! En jij?",
    ],
    "how_are_you": [
        "Ik ben blij dat je het vraagt! Alles goed hier 🚀",
        "Super! Aan het werk en klaar voor jou!",
    ],
    "joke": [
        "Waarom kunnen robots geen geheimen bewaren? Omdat ze alles delen via Bluetooth! 😄",
        "Wat zei de robot tegen de mens? 'Je hebt me gemaakt, nu heb je er spijt van!' 🤖",
    ],
    "music": [
        "Ik kan geen muziek afspelen, maar ik kan wel een liedje neuriën! Zoem zoem... 🎵",
    ],
    "goodbye": [
        "Doei! Tot snel! 👋",
        "Tot ziens! Kom nog eens terug!",
    ],
    "unknown": [
        "Sorry, ik begrijp niet wat je bedoelt 🤔",
        "Kun je dat op een andere manier zeggen?",
        "Hmm, daar heb ik geen antwoord op. Vraag me iets anders!",
    ],
}

# Türkçe yanıtlar
INTENT_RESPONSES_TR = {
    "greeting": [
        "Merhaba! Ben Mini AI Robot! 🐱",
        "Selam! Nasılsın?",
    ],
    "time": ["Saat {time}"],
    "date": ["Bugün {date}"],
    "weather": ["İnternetim yok ama hava güzel görünüyor!"],
    "name": ["Ben Mini AI Robot! Tanıştığımıza memnun oldum!"],
    "how_are_you": ["İyiyim, teşekkürler! Seni görmek güzel 🚀"],
    "joke": ["Robotlar neden dedikodu yapmaz? Çünkü her şeyi kaydederler! 😄"],
    "music": ["Müzik çalamıyorum ama şarkı söyleyebilirim la la la 🎵"],
    "goodbye": ["Görüşürüz! Yine beklerim! 👋"],
    "unknown": ["Anlamadım, tekrar eder misin? 🤔", "Ne dediğini çözemedim!"],
}

# Desteklenen diller
LANGUAGES = {
    "nl": {"name": "Nederlands", "intents": INTENT_RESPONSES_NL},
    "tr": {"name": "Türkçe", "intents": INTENT_RESPONSES_TR},
}
