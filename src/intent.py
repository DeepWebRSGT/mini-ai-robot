"""
Intent Classifier — Coral TPU ile Hızlı Niyet Tanıma
======================================================
Google Coral Edge TPU'da TFLite modeli ile 
anlık metin sınıflandırma. LLM'den ~100× hızlı.
"""

import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    import numpy as np
    from pycoral.utils import edgetpu
    from pycoral.adapters import common
    CORAL_AVAILABLE = True
except ImportError:
    CORAL_AVAILABLE = False
    logger.warning("Coral TPU kütüphanesi kurulu değil. 'sudo apt install python3-pycoral'")

from config import CORAL


class IntentClassifier:
    """Coral TPU tabanlı intent sınıflandırma"""

    # Niyet → anahtar kelime eşlemesi (TFLite modeli yoksa fallback)
    KEYWORD_INTENTS = {
        "greeting": ["hallo", "hoi", "hey", "goedemorgen", "goedemiddag",
                      "goedeavond", "hi", "merhaba", "selam"],
        "time": ["hoe laat", "tijd", "klok", "hoeveel uur", "saat"],
        "date": ["welke dag", "datum", "vandaag", "tarih", "bugün"],
        "weather": ["weer", "buiten", "regen", "zon", "temperatuur", "hava",
                    "yağmur", "güneş"],
        "name": ["hoe heet", "naam", "wie ben", "adın", "ismin", "sen kimsin"],
        "how_are_you": ["hoe gaat", "alles goed", "met jou", "maak je het",
                        "nasılsın", "iyi misin"],
        "joke": ["grap", "mop", "plezier", "lachen", "şaka", "fıkra"],
        "music": ["muziek", "liedje", "zingen", "şarkı", "müzik", "çal"],
        "goodbye": ["doei", "tot ziens", "dag", "later", "görüşürüz",
                    "hoşçakal", "byebye"],
    }

    def __init__(self):
        self.interpreter = None
        self.intents = list(self.KEYWORD_INTENTS.keys())
        self._setup_coral()

    def _setup_coral(self):
        """Coral TPU'yu başlat (varsa)"""
        if not CORAL_AVAILABLE or not CORAL["enabled"]:
            logger.info("Coral TPU kullanılmıyor (kütüphane yok veya devre dışı)")
            return

        model_file = CORAL["intent_model"]
        import os
        if not os.path.exists(model_file):
            logger.warning(f"Coral model bulunamadı: {model_file}")
            return

        try:
            self.interpreter = edgetpu.make_interpreter(model_file)
            self.interpreter.allocate_tensors()
            logger.info("✅ Coral TPU intent modeli hazır!")
        except Exception as e:
            logger.warning(f"Coral TPU başlatılamadı: {e}")

    def classify(self, text):
        """Metnin niyetini belirle
        
        Önce Coral TPU dener (varsa), keyword fallback kullanır.
        
        Returns:
            str: Intent adı (greeting, time, weather, ...)
        """
        if not text:
            return "unknown"

        text_lower = text.lower().strip()
        
        # Coral TPU ile sınıflandırma
        if self.interpreter:
            coral_intent = self._classify_coral(text_lower)
            if coral_intent:
                return coral_intent

        # Fallback: keyword eşleme
        return self._classify_keyword(text_lower)

    def _classify_coral(self, text):
        """Coral TPU'da TFLite modeli çalıştır"""
        if not self.interpreter:
            return None

        try:
            # Metni tensora çevir (basit bag-of-words veya
            # önceden eğitilmiş embedding gerekli)
            # NOT: Burada gerçek bir TFLite modeliniz olmalı
            input_tensor = common.input_tensor(self.interpreter, 0)
            
            # Model giriş boyutuna göre padding/truncate
            max_len = input_tensor.shape[1]
            char_indices = [min(ord(c) % 128, 127) for c in text[:max_len]]
            char_indices += [0] * (max_len - len(char_indices))
            
            input_tensor[0] = char_indices
            self.interpreter.invoke()
            
            output = common.output_tensor(self.interpreter, 0)
            intent_id = int(np.argmax(output[0]))
            
            if intent_id < len(self.intents):
                return self.intents[intent_id]

        except Exception as e:
            logger.debug(f"Coral sınıflandırma hatası: {e}")

        return None

    def _classify_keyword(self, text):
        """Keyword eşleme ile intent bul"""
        scores = {}
        for intent, keywords in self.KEYWORD_INTENTS.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    score += 1
            if score > 0:
                scores[intent] = score

        if not scores:
            return "unknown"

        # En yüksek skorlu intent
        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]

        # Çok düşük skor → unknown
        if best_score == 1 and len(text) < 5:
            return "unknown"

        return best_intent

    def get_embedding(self, text):
        """Coral ile metin embedding çıkar"""
        if not self.interpreter:
            return None
        # Bu fonksiyon embedding modeliniz varsa çalışır
        return None


class IntentResponder:
    """Niyete göre yanıt üret (LLM kullanmadan)"""

    def __init__(self, language="nl"):
        self.language = language
        self._load_responses()

    def _load_responses(self):
        """Dil bazlı yanıtları yükle"""
        from config import LANGUAGES
        lang_config = LANGUAGES.get(self.language, LANGUAGES["nl"])
        self.responses = lang_config["intents"]

    def respond(self, intent):
        """Niyete göre yanıt seç
        
        Args:
            intent: Intent adı (greeting, time, ...)
        
        Returns:
            str: Yanıt metni
        """
        if intent == "time":
            now = datetime.now()
            time_str = now.strftime("%H:%M")
            if self.language == "nl":
                return f"Het is nu {time_str}."
            else:
                return f"Saat {time_str}."

        if intent == "date":
            now = datetime.now()
            if self.language == "nl":
                date_str = now.strftime("%A %d %B %Y")
                return f"Vandaag is het {date_str}."
            else:
                date_str = now.strftime("%d %B %Y %A")
                return f"Bugün {date_str}."

        responses = self.responses.get(intent, self.responses["unknown"])
        return random.choice(responses)


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    print("🎯 Intent Classifier Test")
    
    classifier = IntentClassifier()
    responder = IntentResponder(language="nl")
    
    test_texts = [
        "Hallo!",
        "Hoe laat is het?",
        "Wat is het weer vandaag?",
        "Hoe heet jij?",
        "Doei!",
        "Vertel eens een grap",
        "Wat is de hoofdstad van Nederland?",  # unknown
    ]
    
    for text in test_texts:
        intent = classifier.classify(text)
        response = responder.respond(intent)
        print(f"  '{text}' → {intent} → '{response}'")
    
    print("✅ Test tamamlandı")
