# 🛠️ Mini AI Robot — EKSİKSİZ KURULUM KILAVUZU

## İÇİNDEKİLER

1. [Malzeme Listesi](#1-malzeme-listesi)
2. [SD Kart Hazırlığı](#2-sd-kart-hazırlığı)
3. [İlk Açılış + Pi'yi Ayarlama](#3-i̇lk-açılış--piyi-ayarlama)
4. [I2S Ses Sistemini Bağlama + Test](#4-i2s-ses-sistemini-bağlama--test)
5. [Yazılım Yükleme](#5-yazılım-yükleme)
6. [AI Modellerini İndirme](#6-ai-modellerini-i̇ndirme)
7. [Projeyi Klonlama + Çalıştırma](#7-projeyi-klonlama--çalıştırma)
8. [Ekran Bağlantısı](#8-ekran-bağlantısı)
9. [Buton + LED Bağlantısı](#9-buton--led-bağlantısı)
10. [Her Şeyi Test Etme](#10-her-şeyi-test-etme)
11. [Kutuya Montaj](#11-kutuya-montaj)
12. [Güç Sistemi](#12-güç-sistemi)
13. [Sorun Giderme](#13-sorun-giderme)
14. [Otomatik Başlatma (İsteyene)](#14-otomatik-başlatma-i̇steyene)

---

## 1) MALZEME LİSTESİ

### Zorunlular

| Parça | Adet | Yaklaşık Fiyat |
|-------|:----:|:--------------:|
| Raspberry Pi 4 Model B (4GB) | 1 | ~€107 |
| 64GB microSD kart (Class 10 / A1) | 1 | ~€12 |
| INMP441 I2S Mikrofon (2'li paket) | 1 set | ~€8 |
| MAX98357A I2S Amplifikatör | 1 | ~€15 |
| 8Ω 1W Mini Hoparlör | 1 | ~€9 |
| 2.8" ILI9341 SPI TFT Ekran | 1 | ~€10 |
| 6x6mm Buton | 1 | ~€4 |
| LED (herhangi renk) | 1 | ~€1 |
| 220Ω Direnç (LED için) | 1 | ~€0.50 |
| PowerBoost 1000C | 1 | ~€11 |
| 3.7V 3000mAh LiPo Batarya | 1 | ~€10 |
| SPDT Kaydırmalı Şalter | 1 | ~€4 |
| Dupont Kablo Seti (M-M, M-V, V-V) | 1 set | ~€7 |
| Breadboard (test için) | 1 | ~€5 |
| USB-C Güç Kablosu | 1 | (varsa kullan) |
| HDMI Kablo + Monitör (ilk kurulum) | 1 | (varsa kullan) |

### Opsiyoneller

- Google Coral USB Accelerator (~€110) — TPU hızlandırma
- Pi Camera Module 3 (~€28) — yüz tanıma
- MPU-6050 IMU (~€6) — hareket algılama
- PETG filament (3D baskı) (~€5)
- M2.5 / M3 vida + ara parça seti (~€8)

---

## 2) SD KART HAZIRLIĞI

> Bunu **kendi bilgisayarında** yap. Pi'ye henüz güç verme.

**Adım 1:** https://www.raspberrypi.com/software/ adresinden **Raspberry Pi Imager**'ı indir ve kur.

**Adım 2:** SD kartı bilgisayarına tak.

**Adım 3:** Raspberry Pi Imager'ı aç.

**Adım 4:** Şunları seç:

```
Raspberry Pi Device: → Raspberry Pi 4
Operating System:    → Raspberry Pi OS (other) → Raspberry Pi OS Lite (64-bit)
                     (Lite = terminal, masaüstü yok. Daha hızlı.
                      Monitör kullanacaksan "with Desktop" seç)
```

**Adım 5:** Sağ alttaki dişli çark (⚙️) butonuna tıkla. Şunları doldur:

```
Hostname:        mini-ai-robot
Kullanıcı adı:   pi
Şifre:           (kendin belirle, unutma!)
WiFi SSID:       (evinin WiFi adı)
WiFi şifre:      (evinin WiFi şifresi)
☑ Enable SSH → Use password authentication
```

**Adım 6:** "SAVE" → "YES" (kartı formatlayacak) → bekle ~5-10 dk.

**Adım 7:** Kart hazır olunca çıkar, Pi'ye tak.

---

## 3) İLK AÇILIŞ + Pİ'Yİ AYARLAMA

**Adım 8:** Pi'ye güç ver. (HDMI monitör + klavye tak, VEYA SSH ile bağlan.)

SSH ile bağlanmak için (WiFi üzerinden):

```
ssh pi@mini-ai-robot.local
# veya
ssh pi@192.168.1.xxx
# (IP adresini router'dan veya "arp -a" ile bul)
```

Şifreni gir.

**Adım 9:** Sistemi güncelle:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget unzip i2c-tools
```

**Adım 10:** Donanım arayüzlerini aç:

```bash
sudo raspi-config
```

Menüde sırayla:
1. **Interface Options** → **SPI** → **Enable**
2. **Interface Options** → **I2C** → **Enable**
3. **Interface Options** → **SSH** → **Enable** (zaten açık)
4. **Performance Options** → **GPU Memory** → **128**
5. **Finish** → **Reboot**

**Adım 11:** Reboot sonrası tekrar SSH bağlan.

**Adım 12:** Ses arayüzünü ekle:

```bash
sudo nano /boot/firmware/config.txt
```

Dosyanın en altına şunu EKLE:

```
# Mini AI Robot ayarları
dtoverlay=googlevoicehat-codec
dtparam=i2s=on
dtparam=spi=on
dtparam=spi_speed=32000000
dtparam=i2c_arm=on
gpu_mem=128
gpio=17=ip,pd
gpio=22=op,dh
```

> Eğer `/boot/firmware/config.txt` yoksa, `/boot/config.txt`'yi dene.

Ctrl+X → Y → Enter ile kaydet.

```bash
sudo reboot
```

**KONTROL:** Tekrar bağlan ve şunu çalıştır:
```bash
ls /dev/i2c-*     # /dev/i2c-1 görmelisin
arecord -l        # Ses kartı listelenmeli
aplay -l          # Ses çıkış kartı listelenmeli
```

---

## 4) I2S SES SİSTEMİNİ BAĞLAMA + TEST

> 🔴 HENÜZ LEHİMLEME YAPMA! Her şeyi breadboard'da dene.

### 4a) INMP441 Mikrofon Bağlantısı

INMP441'in 6 bacağı var. Pi'ye şöyle bağla:

| Mikrofon Pini | Nereye? | Pi Pin | Kablo Rengi |
|---------------|---------|--------|:-----------:|
| **VDD** | → | **Pin 1** (3.3V) | 🔴 Kırmızı |
| **GND** | → | **Pin 6** (GND) | ⚫ Siyah |
| **SCK** (I2S clock) | → | **Pin 12** (GPIO18) | 🟡 Sarı |
| **WS** (word select) | → | **Pin 35** (GPIO19) | 🟡 Sarı |
| **SD** (data out) | → | **Pin 38** (GPIO20) | 🟡 Sarı |
| **L/R** (left/right) | → | **Pin 34** (GND) - sol kanal | ⚫ Siyah |

### 4b) MAX98357A Amplifikatör Bağlantısı

| Amp Pini | Nereye? | Pi Pin | Kablo Rengi |
|----------|---------|--------|:-----------:|
| **VIN** | → | **Pin 2** (5V) | 🔴 Kırmızı |
| **GND** | → | **Pin 14** (GND) | ⚫ Siyah |
| **BCLK** | → | **Pin 12** (GPIO18) | 🟡 Sarı |
| **LRC** | → | **Pin 35** (GPIO19) | 🟡 Sarı |
| **DIN** | → | **Pin 40** (GPIO21) | 🟡 Sarı |

> ⚠️ Mikrofon ve amplifikatör aynı BCLK (GPIO18) ve LRCLK (GPIO19) pinlerini PAYLAŞIR. Bu normaldir.

### 4c) Hoparlör Bağlantısı

| Amp | Hoparlör |
|-----|----------|
| **OUT+** | → Hoparlör (+) (hangi uç olduğu fark etmez) |
| **OUT-** | → Hoparlör (-) |

### 4d) Ses Testi — Mikrofon

```bash
# Kayıt yap (5 saniye):
arecord -d 5 -f S16_LE -r 16000 -c 1 test.wav

# Mikrofona konuş! Sonra kaydı dinle:
aplay test.wav
```

✅ **Kendi sesini duyuyorsan mikrofon çalışıyor.**

### 4e) Ses Testi — Hoparlör

```bash
speaker-test -t sine -f 440 -l 1
```

✅ **"Beeep" sesi duyuyorsan hoparlör çalışıyor.**

Ses seviyesini ayarlamak için:
```bash
alsamixer
```
F6 tuşuna bas → "googlevoicehat" seç → yukarı ok ile sesi aç.

---

## 5) YAZILIM YÜKLEME

```bash
# Önce sistem paketleri:
sudo apt install -y python3-pip python3-venv python3-full \
  portaudio19-dev libatlas-base-dev espeak-ng libsndfile1-dev

# Sanal ortam oluştur:
cd /home/pi
mkdir -p mini-ai-robot && cd mini-ai-robot
python3 -m venv robot-env
source robot-env/bin/activate

# pip'i güncelle:
pip install --upgrade pip

# Python paketlerini kur:
pip install vosk pyaudio piper-tts sounddevice numpy \
  adafruit-circuitpython-rgb-display adafruit-blinka \
  requests
```

> ⚠️ Eğer `pyaudio` hata verirse: `sudo apt install portaudio19-dev` yapıldı mı kontrol et.

**Sadece Coral USB takılıysa:**
```bash
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | \
  sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt update
sudo apt install -y libedgetpu1-max python3-pycoral
```

**Sadece 4GB Pi + LLM istiyorsan:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable ollama
sudo systemctl start ollama
```

---

## 6) AI MODELLERİNİ İNDİRME

```bash
cd /home/pi/mini-ai-robot
source robot-env/bin/activate

# Model klasörü oluştur:
mkdir -p models && cd models

# --- Vosk STT modeli (Hollandaca) ---
wget https://alphacephei.com/vosk/models/vosk-model-small-nl-0.22.zip
unzip vosk-model-small-nl-0.22.zip
rm vosk-model-small-nl-0.22.zip

# --- Piper TTS modeli (Hollandaca kadın sesi) ---
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/nl/nl_NL/glow-tts/medium/nl_NL-glow-tts-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/nl/nl_NL/glow-tts/medium/nl_NL-glow-tts-medium.onnx.json

# --- (OPSİYONEL) Ollama LLM modeli (4GB Pi) ---
ollama pull qwen2.5:0.5b

# --- (OPSİYONEL) Vosk Türkçe model ---
# wget https://alphacephei.com/vosk/models/vosk-model-small-tr-0.3.zip
# unzip vosk-model-small-tr-0.3.zip
# rm vosk-model-small-tr-0.3.zip

cd ..
```

---

## 7) PROJEYİ KLONLAMA + ÇALIŞTIRMA

```bash
cd /home/pi

# Projeyi indir:
git clone https://github.com/DeepWebRSGT/mini-ai-robot.git

# Var olan klasöre kopyala:
cp -r mini-ai-robot/* ~/mini-ai-robot/

# Sanal ortamı aktive et:
cd ~/mini-ai-robot
source robot-env/bin/activate

# Her şeyi test et:
python src/stt.py        # ← Mikrofon testi
python src/tts.py        # ← Hoparlör testi
python src/intent.py     # ← Intent sistemi testi
python src/display.py    # ← Ekran testi
python src/button.py     # ← Buton testi
python src/llm.py        # ← LLM testi (4GB Pi)

# Ana programı çalıştır:
python src/main.py
```

🔴 **2GB Pi kullanıyorsan:** `src/config.py` dosyasını aç ve şu satırı bul:
```python
LLM = {
    "enabled": True,     # → False yap!
```
Bu, sadece intent-based sistemi kullanır (LLM'siz çalışır).

---

## 8) EKRAN BAĞLANTISI

> Ekranı **breadboard testi bitince** bağla, önce ses sistemini hallet.

| TFT Pini | Nereye? | Pi Pin | Kablo |
|----------|---------|--------|:-----:|
| **VCC** | → | **Pin 1** (3.3V) — 5V DEĞİL! | 🔴 |
| **GND** | → | **Pin 6** (GND) | ⚫ |
| **CS** | → | **Pin 24** (GPIO8 / CE0) | 🟣 |
| **RESET** | → | **Pin 18** (GPIO24) | 🟣 |
| **DC** | → | **Pin 22** (GPIO25) | 🟣 |
| **MOSI** | → | **Pin 19** (GPIO10) | 🟣 |
| **SCLK** | → | **Pin 23** (GPIO11) | 🟣 |
| **LED** (arka ışık) | → | **Pin 12** (GPIO18) | 🟡 |

> ⚠️ **EKRANA 5V VERME!** Sadece 3.3V. Yanlış bağlarsan ekranı yakarsın.

Test et:
```bash
python src/display.py
```
✅ Ekranda sırayla ifadeler görmelisin: nötr → mutlu → şaşkın → düşünen → aşık → üzgün → kızgın → uyku.

---

## 9) BUTON + LED BAĞLANTISI

### Buton

| Buton | Pi Pin |
|-------|--------|
| 1. uç | **Pin 11** (GPIO17) |
| 2. uç | **Pin 14** (GND) |

> GPIO17'de iç pull-up var. Harici direnç gerekmez.

### LED

| LED | Nereye? | Pi Pin |
|-----|---------|--------|
| **Anot** (+ uzun bacak) | → **220Ω direnç** → | **Pin 15** (GPIO22) |
| **Katot** (- kısa bacak) | → | **Pin 34** (GND) |

> ⚠️ **220Ω DİRENÇ KULLANMAZSAN GPIO'YU YAKARSIN!**

Test et:
```bash
python src/button.py
```
✅ LED 2 kere yanıp söner. Butona basınca LED yanar.

---

## 10) HER ŞEYİ TEST ETME

Son entegrasyon testi:

```bash
cd ~/mini-ai-robot
source robot-env/bin/activate
python src/main.py
```

Şu mesajı görmelisin:
```
🤖 Mini AI Robot başlatılıyor...
✅ Buton ve LED hazır
✅ Ekran hazır
✅ STT (Vosk) hazır
✅ TTS (Piper) hazır
✅ Intent sınıflandırıcı hazır
✅ LLM hazır — akıllı mod aktif!
🤖 Robot hazır! Butona bas ve konuş.
```

**Dene:**
- Butona bas → "Hallo!" de → Robot gülümser ve "Hallo! Ik ben Mini AI Robot!" der
- "Hoe laat is het?" → Saati söyler
- "Vertel een grap" → Şaka yapar
- "Doei!" → Veda eder

---

## 11) KUTUYA MONTAJ

**Sıralama:**

1. **ÖNCE gücü KES** (Pi'yi kapat, fişi çek)
2. Breadboard'daki her bağlantının **fotoğrafını çek**
3. Kabloları tek tek sök
4. Pi'yi kutu tabanına vidalarla sabitle (M2.5 vida + ara parça)
5. PowerBoost'u Pi'nin yanına bantla/vidalarla sabitle
6. LiPo bataryayı en alta koy (hareket etmeyecek şekilde)
7. Şalteri kutunun yan yüzüne monte et
8. Ekranı ön yüze monte et
9. Mikrofonu üst/ön kısma (ses alacak yere) — küçük delik aç
10. Amplifikatör + hoparlörü yan veya alt kısma
11. Butonu yan yüzde kolay erişilecek yere
12. LED'i ön yüzde görülecek yere
13. Tüm kabloları düzenle, zip tie ile topla

**Montaj sonrası ilk açılış:**
1. Şalteri aç → PowerBoost'ta LED yanmalı
2. Pi açılır (~30 sn)
3. Butona bas → robot çalışıyor mu?

---

## 12) GÜÇ SİSTEMİ

**Kablo bağlantısı:**
```
LiPo (+) → SPDT şalter → PowerBoost BAT(+) 
LiPo (-) → PowerBoost BAT(-)
PowerBoost 5V → Pi USB-C güç girişi (5V pin'e değil!)
PowerBoost GND → Pi GND
```

**Şarj etme:** PowerBoost'un USB-C portuna kablo tak. LED yanar, dolunca söner (~3 saat). Şarj ederken şalter KAPALI olsun.

**Pil ömrü (3000mAh ile):**
- Bekleme (buton beklemede): ~5 saat
- Aktif konuşma: ~2-3 saat
- LLM çalışırken (4GB Pi): ~1.5-2 saat

> ⚠️ **LiPo güvenliği:** Delme, ezme, ıslatma! Şişerse kullanma. Yangın riski var!

---

## 13) SORUN GİDERME

### Ses gelmiyor?
```
1. speaker-test -t sine -f 440 -l 1  → ses var mı?
2. MAX98357A 5V alıyor mu? (Pin 2'ye bağlı mı?)
3. config.txt'ye dtoverlay=googlevoicehat-codec eklendi mi, reboot yapıldı mı?
4. alsamixer → F6 ile doğru kartı seç → ses seviyesini yukarı al
```

### Vosk "model bulunamadı" hatası?
```
ls ~/mini-ai-robot/models/
# vosk-model-small-nl-0.22/ klasörü var mı?
```

### Ekran beyaz / boş?
```
ls /dev/spi*   # spi cihazları görünüyor mu?
# raspi-config'de SPI Enable mı?
# Ekrana 3.3V gidiyor mu? (5V değil!)
```

### Buton çalışmıyor?
```python
python -c "
import RPi.GPIO as g
g.setmode(g.BCM)
g.setup(17, g.IN, pull_up_down=g.PUD_UP)
print(g.input(17))  # basılı değilken 1, basılıyken 0
"
```

### Ollama çok yavaş?
```
# 4GB Pi kullanıyor musun? 2GB Pi'de LLM çalışmaz!
# İlk soru her zaman yavaştır (model RAM'e yüklenir)
# Daha küçük model: ollama pull tinyllama:1.1b-q4
```

### "ImportError: No module named 'board'"?
```
pip install adafruit-blinka
pip install adafruit-circuitpython-rgb-display
```

### Hiçbir şey çalışmıyorsa:
SD kartı bilgisayara tak, Raspberry Pi Imager ile sıfırdan yaz, Adım 1'den başla.

---

## 14) OTOMATİK BAŞLATMA (İSTEYENE)

Pi'yi açınca robot kendiliğinden başlasın istiyorsan:

**Servis dosyası oluştur:**

```bash
sudo nano /etc/systemd/system/mini-ai-robot.service
```

İçine şunu yapıştır:

```
[Unit]
Description=Mini AI Robot
After=network.target sound.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/mini-ai-robot
Environment="PATH=/home/pi/mini-ai-robot/robot-env/bin:/usr/bin:/bin"
ExecStart=/home/pi/mini-ai-robot/robot-env/bin/python src/main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Kaydet (Ctrl+X → Y → Enter) ve aktif et:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mini-ai-robot.service
sudo systemctl start mini-ai-robot.service
```

**Kontrol:**
```bash
sudo systemctl status mini-ai-robot.service
# "active (running)" yazmalı
```

**Hata varsa:**
```bash
sudo journalctl -u mini-ai-robot.service -n 20
```

**Durdurmak için:**
```bash
sudo systemctl stop mini-ai-robot.service
```

---

## ✅ KONTROL LİSTESİ (Hepsi tamam mı?)

- [ ] SD kart hazır, Pi OS yüklü
- [ ] SSH ile bağlanabiliyorum
- [ ] SPI, I2C, I2S etkin
- [ ] config.txt düzenlendi, reboot yapıldı
- [ ] Hoparlörden ses geliyor
- [ ] Mikrofondan kayıt alınıyor
- [ ] Python venv kurulu, pip paketleri yüklü
- [ ] Vosk + Piper modelleri indirildi
- [ ] STT testi: konuşunca metin çıkıyor
- [ ] TTS testi: yazınca ses çıkıyor
- [ ] Ekran testi: yüz ifadeleri görünüyor
- [ ] Buton testi: basınca LED yanıyor
- [ ] Ana program çalışıyor, robot konuşuyor
- [ ] Kutuya monte edildi
- [ ] Güç sistemi bağlandı
- [ ] Kapatıp açtım, hala çalışıyor

---

**Hepsi tamam mı? TEBRİKLER! Robotun hazır! 🤖🎉**
