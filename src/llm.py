"""
LLM (Large Language Model) — Ollama ile Offline AI
====================================================
Raspberry Pi'de çalışan küçük dil modeli ile doğal dil işleme.
"""

import json
import logging
import subprocess
import requests

logger = logging.getLogger(__name__)

from config import LLM


class LocalLLM:
    """Ollama üzerinden lokal LLM çağrıları"""

    def __init__(self, model=None, host=None):
        self.model = model or LLM["model"]
        self.host = host or LLM["host"]
        self.system_prompt = LLM["system_prompt"]
        self.available = False
        self._check_ollama()

    def _check_ollama(self):
        """Ollama'nın çalışıp çalışmadığını kontrol et"""
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=3)
            if r.status_code == 200:
                models = [m["name"] for m in r.json().get("models", [])]
                if self.model in models:
                    self.available = True
                    logger.info(f"✅ Ollama hazır — model: {self.model}")
                else:
                    logger.warning(
                        f"Model '{self.model}' bulunamadı. "
                        f"Çalıştır: ollama pull {self.model}"
                    )
                    logger.info(f"Mevcut modeller: {', '.join(models[:5])}")
            else:
                logger.warning("Ollama API yanıt vermedi")
        except requests.ConnectionError:
            logger.warning(
                "Ollama çalışmıyor. Çalıştır: 'ollama serve' veya "
                "'sudo systemctl start ollama'"
            )
        except Exception as e:
            logger.warning(f"Ollama kontrolü başarısız: {e}")

    def ask(self, prompt, max_tokens=128):
        """LLM'ye soru sor
        
        Args:
            prompt: Kullanıcı sorusu
            max_tokens: Maksimum yanıt uzunluğu
        
        Returns:
            str: Model yanıtı
        """
        if not self.available:
            logger.warning("LLM kullanılamıyor, intent-based yanıt kullan")
            return ""

        full_prompt = f"{self.system_prompt}\n\nGebruiker: {prompt}\nRobot:"
        
        try:
            r = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.7,
                    }
                },
                timeout=LLM["timeout"],
            )

            if r.status_code == 200:
                response = r.json().get("response", "").strip()
                logger.debug(f"LLM yanıtı: {response}")
                return response
            else:
                logger.error(f"Ollama hata: {r.status_code}")
                return ""

        except requests.Timeout:
            logger.warning("LLM zaman aşımı (model çok yavaş olabilir)")
            return ""
        except Exception as e:
            logger.error(f"LLM hatası: {e}")
            return ""

    def ask_stream(self, prompt, on_token=None):
        """LLM'den akışlı yanıt al (karakter karakter)"""
        if not self.available:
            return ""

        full_prompt = f"{self.system_prompt}\n\nGebruiker: {prompt}\nRobot:"
        response = ""

        try:
            r = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": True,
                },
                stream=True,
                timeout=LLM["timeout"],
            )

            for line in r.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        token = data.get("response", "")
                        response += token
                        if on_token:
                            on_token(token)
                        if data.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            logger.error(f"LLM akış hatası: {e}")

        return response.strip()

    def get_embedding(self, text):
        """Metin embedding'i al (similarity/search için)"""
        if not self.available:
            return None

        try:
            r = requests.post(
                f"{self.host}/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": text,
                },
                timeout=10,
            )
            if r.status_code == 200:
                return r.json().get("embedding", [])
        except Exception:
            pass
        return None


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    print("🧠 LLM Test")
    
    llm = LocalLLM()
    if llm.available:
        response = llm.ask("Hoe gaat het met je?")
        print(f"  → {response}")
    else:
        print("  → Ollama çalışmıyor veya model yok")
    print("✅ Test tamamlandı")
