# Mini AI Robot — Detaylı Parça Listesi

## Zorunlu Parçalar

| # | Parça | Fiyat | Adet | Satın Alma |
|---|-------|:-----:|:----:|:----------:|
| 1 | Raspberry Pi 4 Model B (4GB) | ~€107 | 1 | [kiwi-electronics.com](https://www.kiwi-electronics.com/nl/raspberry-pi-4-model-b-4gb-4268?country=NL) |
| 2 | Waveshare 2.8" ILI9341 SPI TFT 240×320 (touch) | ~€10 | 1 | [Amazon.nl](https://www.amazon.nl/DollaTek-ILI9341-Display-Seri%C3%ABle-Module/dp/B082QVKT7M) |
| 3 | INMP441 I2S MEMS Mikrofon (2'li paket) | ~€8 | 1 set | Amazon.nl |
| 4 | Adafruit MAX98357A I2S 3W Amplifikatör | ~€15 | 1 | Amazon.nl |
| 5 | 8Ω 1W Mini Metal Speaker | ~€9 | 1 | [Amazon.nl](https://www.amazon.nl/CQRobot-Luidspreker-Dupont-interface-verscheidenheid-elektronische/dp/B0822YL2L2) |
| 6 | 6×6mm Momentary Buton | ~€4 | 1 | [Amazon.nl](https://www.amazon.nl/Youmile-Miniatuur-Momentary-Drukknopschakelaar-Kwaliteitsschakelaar/dp/B07Q1BXV7T) |
| 7 | 3.7V 3000mAh LiPo Batarya | ~€10 | 1 | [Amazon.nl](https://www.amazon.nl/lithium-polymeerbatterij-doe-het-zelf-elektronische-batterijvervanging-LED-verlichting/dp/B0F3CZ72C6) |
| 8 | Adafruit PowerBoost 1000C (USB-C LiPo şarj + 5V boost) | ~€11 | 1 | [Amazon.nl](https://www.amazon.nl/YINETTECH-Overcharge-Protection-Battery-Powered-Equipment/dp/B0CXSY2XSJ) |
| 9 | SPDT Kaydırmalı Güç Anahtarı | ~€4 | 1 | [Amazon.nl](https://www.amazon.nl/Youmile-mini-verticale-schuifschakelaars-schuifschakelaar-vergrendelende/dp/B08SM2HHNR) |
| 10 | PETG Filament beyaz 1kg | ~€5 | 1 | Amazon.nl / bol.com |
| 11 | Dupont Jumper Kablolar (M-M / M-V / V-V) | ~€7 | 1 set | Amazon.nl |
| 12 | SanDisk Ultra microSD 64GB Class 10 A1 | ~€12 | 1 | Amazon.nl / bol.com / Action |
| 13 | M2.5 + M3 Pirinç Ara Parça + Vida Seti | ~€8 | 1 set | [Amazon.nl](https://www.amazon.nl/Schroevenset-zeskantschroeven-lenskopschroeven-cilinderschachtschroeven-koolstofstaal/dp/B0CY1YZZC8) |

## Opsiyonel Parçalar

| Parça | Fiyat | Açıklama |
|-------|:-----:|:---------|
| Google Coral USB Accelerator (Edge TPU) | ~€110 | TPU hızlandırma, 4 TOPS INT8 |
| Raspberry Pi Kamera Module 3 (CSI, 12MP) | ~€28 | Yüz/el tanıma |
| MPU-6050 IMU (GY-521, 6-DOF) | ~€6 | Hareket/tik algılama |

## Bağlantı Şeması

```
Raspberry Pi 4 GPIO
====================

[I2S Ses Çıkışı → MAX98357A]
GPIO18 (BCLK)  → MAX98357A BCLK
GPIO19 (LRCK)  → MAX98357A LRC
GPIO21 (DIN)   → MAX98357A DIN
5V             → MAX98357A VIN
GND            → MAX98357A GND
Speaker        → MAX98357A OUT+ / OUT-

[I2S Ses Girişi → INMP441]
GPIO18 (BCLK)  → INMP441 SCK
GPIO19 (LRCK)  → INMP441 WS
GPIO20 (DOUT)  → INMP441 SD
3.3V           → INMP441 VDD
GND            → INMP441 GND

[SPI Ekran → ILI9341]
GPIO8  (CE0)   → TFT CS
GPIO10 (MOSI)  → TFT MOSI
GPIO11 (SCLK)  → TFT SCK
GPIO25 (D/C)   → TFT DC
GPIO24 (RST)   → TFT RST
GPIO18 (PWM)   → TFT LED (backlight)
3.3V           → TFT VCC
GND            → TFT GND

[Buton]
GPIO17         → Buton bir ucu
GND            → Buton diğer ucu

[LED]
GPIO22         → LED anot (+)
GND            → LED katot (-) (220Ω direnç ile)

[I2C → MPU-6050 (Opsiyonel)]
GPIO2  (SDA)   → MPU-6050 SDA
GPIO3  (SCL)   → MPU-6050 SCL
3.3V           → MPU-6050 VCC
GND            → MPU-6050 GND

[CSI Kamera (Opsiyonel)]
Pi Camera Module 3 → CSI portuna doğrudan takılır

[Güç]
PowerBoost 5V  → Pi 4 USB-C güç girişi (VCC + GND)
PowerBoost GND → Pi 4 GND
PowerBoost Bat → LiPo Batarya +
PowerBoost GND → LiPo Batarya -
SPDT Switch    → PowerBoost ile batarya arasında kesme
```
