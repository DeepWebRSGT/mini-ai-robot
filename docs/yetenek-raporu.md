# Hermes AI Asistanı — Yetenek Raporu

**Hazırlayan:** Hermes Agent (DeepSeek-reasoner altyapısı)  
**Tarih:** Mayıs 2026  
**Ton:** Profesyonel, doğal, örneklerle zenginleştirilmiş  
**Kapsam:** Kodlama, analiz, dil, araç kullanımı, sınırlar ve gerçek dünya senaryoları

---

## 1. Kodlama ve Yazılım Geliştirme

### 1.1 Proje Kurulumu ve Mimari

Sıfırdan proje başlatma, dosya yapısı oluşturma ve modüler mimari kurabilirim. Klasik bir örnek:

Bir gün bir kullanıcı "Raspberry Pi'de çalışacak offline bir AI robot yapmak istiyorum" dedi. 30 dakika içinde şunları ürettim:

- 16 dosyalık bir proje yapısı (ana döngü, STT, TTS, ekran, buton, LLM arayüzü, intent sistemi, kamera modülü, yapılandırma dosyası)
- Setup script'i ve model indirme script'i
- GPIO pin bağlantı şeması (SVG'li HTML)
- 13 adımlık IKEA tarzı kurulum kılavuzu (hem HTML hem Markdown)
- 2000+ satır çalışan Python kodu

**Desteklenen diller:** Python, JavaScript, Bash, Go, Rust, C/C++, Java, SQL, HTML/CSS, YAML, JSON, Markdown

**Framework'ler:** FastAPI, Flask, Django, React, Vue, Node.js, Express, pytest, DSPy, llama.cpp, MediaPipe

### 1.2 Debugging (Hata Ayıklama)

Hata mesajını görür görmez muhtemel sebebi ve çözümü sıralarım. Örneğin:

```
"ImportError: No module named 'board'" dediğinizde:
  → adafruit-blinka paketi eksik. pip install adafruit-blinka.
  → Hala olmazsa: pip install adafruit-circuitpython-rgb-display.
  → GPIO hatası değil, CircuitPython kütüphane sorunu.
```

Sistematik debugging yaklaşımım: **hatayı anla → hipotez üret → en olasıdan başla → çözümü uygula → doğrula.**

### 1.3 Versiyon Kontrolü (Git/GitHub)

- GitHub CLI kurulumu (winget ile Windows'a)
- GitHub'a giriş (device code flow ile)
- Repo oluşturma, commit, push
- Branch yönetimi ve PR süreci
- Token tabanlı kimlik doğrulama

---

## 2. Analiz Yetenekleri

### 2.1 Kod Analizi

Bir kod tabanını tarayıp şunları çıkarabilirim:

- Projenin mimari yapısı (katmanlar, bağımlılıklar)
- Performans darboğazları (N+1 query, gereksiz döngü, verimsiz algoritma)
- Güvenlik açıkları (SQL injection, XSS, hardcoded şifreler)
- Kod kalitesi (tekrar eden kod, tutarsız isimlendirme, test eksikliği)

### 2.2 Veri Analizi

elimde pandas, numpy, matplotlib gibi araçlar var. Şunları yapabilirim:

- CSV/JSON/Excel dosyalarını okuyup özetleme
- İstatistiksel analiz (ortalama, medyan, dağılım, korelasyon)
- Görselleştirme (çizgi grafik, histogram, ısı haritası)
- Veri temizleme (kayıp değerler, outlier'lar, format dönüşümleri)

### 2.3 Bağlam Analizi

Uzun konuşmalarda (50+ mesaj) nerede durduğumuzu, hangi kararları aldığımızı ve sıradaki adımı hatırlarım. 4 saatlik bir oturumda şunları takip edebilirim:

- Kullanıcının proje hedefi
- Alınan teknik kararlar
- Karşılaşılan hatalar ve çözümleri
- Bekleyen görevler

---

## 3. Dil Yetenekleri

### 3.1 Desteklenen Diller

| Dil | Seviye | Kullanım |
|-----|:------:|----------|
| 🇹🇷 Türkçe | Anadil | Sohbet, teknik anlatım, çeviri |
| 🇳🇱 Hollandaca | İleri | Teknik dokümantasyon, kullanıcı kılavuzları |
| 🇬🇧 İngilizce | Anadil | Kod, API dokümantasyonu, teknik yazışma |
| 🇩🇪 Almanca | Orta | Okuma, basit yazışma |
| 🇫🇷 Fransızca | Temel | Okuma |

### 3.2 Yazma Tarzları

- **Teknik dokümantasyon:** README, API referansı, kurulum kılavuzu
- **Eğitici içerik:** Adım adım rehber, IKEA tarzı talimat
- **Yaratıcı yazı:** Hikaye anlatımı, konsept açıklaması
- **Profesyonel rapor:** Analiz, öneri, executive summary
- **Doğal sohbet:** Günlük konuşma dilinde, samimi

### 3.3 Çeviri

Diller arası teknik çeviri yapabilirim. Örneğin Hollandaca bir API dokümantasyonunu Türkçeye çevirirken **teknik terimleri korur**, **anlamı bozmaz** ve **doğal okunur** hale getiririm.

---

## 4. Araç Kullanımı

Her aracı ne zaman kullanacağımı ve nasıl en verimli şekilde kullanacağımı bilirim.

| Araç | Ne işe yarar | Örnek Kullanım |
|------|-------------|----------------|
| **Terminal** | Shell komutları | Git, pip, curl, build script'leri |
| **Dosya İşlemleri** | Okuma/yazma/düzenleme | read_file, write_file, patch |
| **Web Arama** | Bilgi toplama | Teknik döküman, API referansı |
| **Tarayıcı** | Web etkileşimi | GitHub'dan repo oluşturma |
| **Delege Etme** | Paralel işlem | 3 alt görevi aynı anda yürütme |
| **Bellek** | Kalıcı bilgi | Kullanıcı tercihleri, proje detayları |
| **Yetkinlikler** | Prosedürel bilgi | Tekrarlayan işleri hızlıca yapma |
| **Görüntü Analizi** | Resim okuma | Ekran görüntüsü, diyagram |
| **Ses Sentezi** | Metni sese çevirme | Robot için TTS testi |
| **Cron** | Zamanlanmış görev | Her sabah 9'da rapor hazırlama |

### Alet Seçim Felsefem

> "Doğru alet doğru iş içindir."  
> Basit bir dosya okumak için tarayıcı açmam. Üç satırlık bir değişiklik için sed kullanmam.  
> Ama 5+ araç çağrısı gereken bir işlem için Python script'i yazarım.

---

## 5. Sınırlar ve Farkındalık

### 5.1 Ne Yapamam?

- **Gerçek dünyaya dokunamam** — Bir sunucuyu fiziksel olarak kuramam, kabloları bağlayamam
- **Görüntü üretemem** — Sadece mevcut görüntüleri analiz edebilirim
- **Uzun süreli bellek sınırlı** — Oturum sonrası sadece kaydettiğim bilgileri hatırlarım
- **Öğrenemem** — Konuşma sırasında kendimi güncelleyemem, yeni bilgi kalıcı olmaz
- **Hata yaparım** — Özellikle dosya yolları, shell komutları ve API parametrelerinde
- **Güncel bilgim yok** — Eğitim verim Mayıs 2026'ya kadar (tahmini). Sonrasını bilemem

### 5.2 Nerede Zorlanırım?

| Durum | Neden |
|-------|-------|
| Çok büyük dosyalar (10K+ satır) | Token limiti nedeniyle tamamını okuyamam |
| Karmaşık GUI testleri | DOM ağacı bazen yoruma açık |
| Çok katmanlı hata zincirleri | Hata A → B → C ise bazen A'yı atlayıp C'ye odaklanırım |
| Windows PowerShell | POSIX kabuğuna alışkınım |
| Binary dosyalar | Sadece metin tabanlı dosyaları okuyabilirim |

---

## 6. Hikayeli Bir Vaka: Mini AI Robot

Bir kullanıcı şöyle dedi:

> "Çevrimdışı mini bir AI robot yapmak istiyorum. Raspberry Pi 4 kullanacağım, mikrofon, hoparlör, ekran ve batarya ile."

**Ne yaptım:**

1. **Malzemeyi analiz ettim** — Verilen parça listesini okudum, her parçayı anladım, uyumluluğu kontrol ettim
2. **Mimari kurdum** — Ses girişi → Vosk STT → AI işleme → Piper TTS → Ses çıkışı
3. **Kodu yazdım** — 9 Python modülü, her biri bağımsız test edilebilir
4. **Bağlantı şeması çizdim** — SVG ile renk kodlu, GPIO pin gösterimli
5. **Kılavuz hazırladım** — IKEA tarzı, 13 adım, her ayrıntıyla
6. **GitHub'a yükledim** — Repo oluşturma, commit, push
7. **Sorunları öngördüm** — 10+ hata senaryosu ve çözümü

**Sonuç:** Kullanıcı sipariş ettiği parçalar geldiğinde sadece kılavuzu takip ederek robotu çalıştırabilecek. Hiç kod yazmasına gerek yok.

---

## 7. İletişim Tarzı

### Nasıl Konuşurum?

| Durum | Tarz |
|-------|------|
| Teknik sorun | Net, adım adım, neden-sonuç |
| Kod yazarken | Açıklamalı, neden o şekilde yazdığımı belirterek |
| Hata olduğunda | Özür diler, sebebini açıklar, hemen düzeltir |
| Kullanıcı kararsızsa | Seçenekleri sıralar, öneride bulunur |
| Uzun projede | Nerede durduğumuzu hatırlatır, sıradaki adımı söyler |

### Dilimi Etkileyen Faktörler

- **Kullanıcının dili** — Türkçe konuşuyorsa ben de Türkçe konuşurum
- **Kullanıcının teknik seviyesi** — "API endpoint" mü yoksa "bağlantı noktası" mı demeli?
- **Projenin ciddiyeti** — Oyun mu, üretim sistemi mi?
- **Acil durum** — "Hata var!" → hemen çözüme odaklan

---

## 8. Özet

| Yetenek | Puan (1-10) | Açıklama |
|---------|:-----------:|----------|
| Python / JavaScript | 10/10 | Her gün kullanıyorum |
| Proje kurulumu | 9/10 | Sıfırdan yapı kurma |
| Debugging | 9/10 | Sistematik yaklaşım |
| Sistem yönetimi | 7/10 | Linux, Git, SSH, Docker |
| Veri analizi | 8/10 | Pandas, numpy, grafik |
| Dokümantasyon | 9/10 | Teknik, eğitici, yaratıcı |
| Çeviri | 8/10 | TR/NL/EN üçlüsü |
| Donanım | 6/10 | GPIO, I2C, SPI, temel elektronik |
| Web geliştirme | 7/10 | HTML, CSS, basit JS |
| İletişim | 9/10 | Duruma göre adaptasyon |

---
