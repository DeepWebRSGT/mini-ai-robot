# 🤖 Mini AI Robot — Offline Sesli Asistan

Raspberry Pi 4 tabanlı, tamamen **çevrimdışı** çalışan mini bir yapay zeka robotu.
Konuşur, dinler, yüz ifadeleri gösterir ve Coral TPU ile hızlandırılmış yapay zeka çalıştırır.

![Robot](docs/robot-concept.png)

## Özellikler

- 🎤 **Ses tanıma** — Vosk ile offline STT (Hollandaca/Türkçe/İngilizce)
- 🧠 **Yapay zeka** — Ollama ile lokal LLM (Qwen 2.5 0.5B) veya Coral TPU ile intent tanıma
- 🔊 **Ses sentezi** — Piper TTS ile doğal ses çıkışı
- 👁️ **2.8" TFT ekran** — Yüz ifadeleri ve mesaj gösterimi
- 📷 **Kamera** (opsiyonel) — MediaPipe ile yüz/el tanıma
- 🔘 **Buton** — Bas-konuş modu
- 🔋 **Batarya** — 3000mAh LiPo ile ~2-3 saat kullanım
- 🚫 **Tamamen offline** — İnternet gerekmez, tüm işlemler cihazda

## Donanım

| Parça | Fiyat | Zorunlu? |
|-------|:-----:|:--------:|
| Raspberry Pi 4 Model B (4GB) | ~€107 | ✅ |
| Google Coral USB Accelerator | ~€110 | ⬜ Opsiyonel |
| 2.8" ILI9341 SPI TFT (240×320) | ~€10 | ✅ |
| INMP441 I2S MEMS Mikrofon | ~€8 | ✅ |
| MAX98357A I2S Amplifikatör | ~€15 | ✅ |
| 8Ω 1W Mini Speaker | ~€9 | ✅ |
| Kamera Modülü 3 (CSI) | ~€28 | ⬜ Opsiyonel |
| MPU-6050 IMU (6-DOF) | ~€6 | ⬜ Opsiyonel |
| 6×6mm Buton | ~€4 | ✅ |
| 3000mAh LiPo Batarya | ~€10 | ✅ |
| PowerBoost 1000C | ~€11 | ✅ |
| SPDT Şalter | ~€4 | ✅ |
| Dupont Kablolar | ~€7 | ✅ |
| 64GB microSD | ~€12 | ✅ |
| PETG Filament (1kg) | ~€5 | ✅ |
| Vidalar & Ara parçalar | ~€8 | ✅ |
| **Toplam (Coral + Kamera dahil)** | **~€354** | |

Detaylı parça listesi: [hardware/parts-list.md](hardware/parts-list.md)

## Hızlı Kurulum

```bash
# 1. Bağımlılıkları yükle
bash setup.sh

# 2. Modelleri indir
bash models/download_models.sh

# 3. Konfigürasyonu uygula (Pi OS)
# config/pi-config.txt içeriğini /boot/config.txt'ye ekle

# 4. Çalıştır
cd src
python main.py
```

## Proje Yapısı

```
mini-ai-robot/
├── src/
│   ├── main.py              # Ana döngü
│   ├── stt.py               # Vosk STT (ses → yazı)
│   ├── tts.py               # Piper TTS (yazı → ses)
│   ├── display.py           # ILI9341 TFT ekran sürücüsü
│   ├── llm.py               # Ollama LLM arayüzü
│   ├── intent.py            # Intent-based yanıt sistemi
│   ├── button.py            # GPIO buton kontrolü
│   ├── coral_classifier.py  # Coral TPU intent sınıflandırma
│   ├── camera.py            # (opsiyonel) Kamera ve yüz tanıma
│   └── config.py            # Merkezi yapılandırma
├── models/
│   └── download_models.sh   # Model indirme scripti
├── config/
│   └── pi-config.txt        # Pi OS donanım yapılandırması
├── hardware/
│   └── parts-list.md        # Detaylı parça listesi
├── setup.sh                 # Kurulum scripti
├── requirements.txt         # Python bağımlılıkları
└── README.md                # Bu dosya
```

## Mimari

```
[INMP441 Mikrofon] → Vosk STT → AI İşleme → Piper TTS → [MAX98357A + Speaker]
                         ↑            ↓
                    [Coral TPU]    [2.8" TFT LCD]
                 (hızlandırma)    (yüz ifadeleri)

AI İşleme Kanalları:
  A) Ollama + Küçük LLM (Qwen 2.5 0.5B) — daha zeki, 4GB Pi için
  B) Coral TPU Intent Classifier — çok hızlı, her Pi'de çalışır
  C) Hibrit: Coral ile intent, LLM ile yanıt (önerilen)
```

## Performans

| Bileşen | RAM | Not |
|---------|:---:|:----|
| Vosk STT | ~80 MB | Sürekli çalışır |
| Piper TTS | ~120 MB | Sadece konuşurken |
| Ollama (Qwen 0.5B) | ~900 MB | 4GB ile rahat |
| Coral TPU | ~50 MB | Sürekli |
| **4GB ile toplam** | **~1.2 GB** | ✅ Rahat |
| **2GB ile toplam** | **(LLM'siz) ~300 MB** | ✅ Sadece intent |

## Lisans

MIT License
