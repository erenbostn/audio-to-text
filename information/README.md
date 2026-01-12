# GroqWhisper Desktop - Bilgi Bankası

Bu klasör, GroqWhisper Desktop uygulamasının tüm modüllerini, dosyalarını ve sistemlerini açıklayan kapsamlı dokümantasyon içerir.

---

## 📁 Dokümanlar

| Dosya | Konu | Açıklama |
|-------|------|----------|
| **[core.md](core.md)** | Çekirdek Modüller | `recorder`, `transcriber`, `input_simulator`, `history_manager` |
| **[ui.md](ui.md)** | Kullanıcı Arayüzü | `overlay`, `settings_window`, `tray` |
| **[models.md](models.md)** | Veri Modelleri | `Recording` dataclass ve özellikleri |
| **[main.md](main.md)** | Ana Uygulama | `config`, `main` - başlatma ve orkestrasyon |
| **[utils.md](utils.md)** | Yardımcı Fonksiyonlar | `sound_feedback` |

---

## 🗂️ Proje Yapısı

```
audio_to_text/
├── src/
│   ├── core/              # Çekirdek işlevselliği
│   │   ├── recorder.py         # Ses kaydedici
│   │   ├── transcriber.py      # Groq API transkripsiyon
│   │   ├── input_simulator.py   # Metin enjektörü
│   │   └── history_manager.py   # Kayıt geçmişi
│   │
│   ├── models/            # Veri modelleri
│   │   └── recording.py         # Recording dataclass
│   │
│   ├── ui/                # Kullanıcı arayüzü
│   │   ├── overlay.py           # Kayıt durumu penceresi
│   │   ├── settings_window.py   # Ana ayarlar penceresi
│   │   └── tray.py              # Sistem tepsisi
│   │
│   ├── utils/             # Yardımcı fonksiyonlar
│   │   └── sound_feedback.py    # Bip sesleri
│   │
│   ├── config.py          # .env yönetimi
│   └── main.py            # Ana uygulama döngüsü
│
├── temp/                   # Geçici ses dosyaları (oturum boyunca)
├── docs/                   # Proje dokümantasyonu
├── information/            # BURADASINIZ (bilgi bankası)
└── requirements.txt        # Python bağımlılıkları
```

---

## 🔄 Uygulama Akışı

```
1. BAŞLATMA
   python src/main.py
   │
   ├─→ Config yükle (.env'den API key)
   ├─→ Core modülleri başlat
   ├─→ SettingsWindow AÇ (ana pencere)
   └─→ Hotkey listener başlat (Ctrl+Alt+K)

2. SES KAYDETME
   Ctrl+Alt+K veya UI butonu
   │
   ├─→ start_recording()
   ├─→ Overlay göster (yüzen pencere)
   ├─→ Bip sesi (1000Hz)
   └─→ Temp klasörüne .wav olarak kaydet

3. KAYIT DURDURMA
   Ctrl+Alt+K veya UI butonu
   │
   ├─→ stop_recording()
   ├─→ Overlay gizle
   ├─→ Bip sesi (700Hz)
   └─→ Kaydı HISTORY'ye ekle (transkribe ETMEZ!)

4. TRANSKRİPSİYON
   History'den seç → "Transcribe Selected"
   │
   ├─→ Seçili .wav dosyalarını al
   ├─→ Groq API'ye gönder (whisper-large-v3)
   ├─→ Transkribe metnini al
   └─→ Metni aktif pencereye yapıştır (clipboard)

5. DOSYA YÜKLEME
   "Browse" → dosya seç → "Transcribe File"
   │
   ├─→ File dialog'dan dosya seç
   ├─→ Groq API'ye gönder
   └─→ Sonucu yapıştır

6. KAPATMA
   X butonu veya Ctrl+Alt+Q
   │
   ├─→ Pencereyi gizle (tray'e küçült)
   ├─→ Hotkey'ler çalışmaya devam
   └─→ Quit'ten → temp dosyaları sil + çık
```

---

## 🔑 Temel Kavramlar

### Recording (Kayıt)
- Mikrofondan yakalanan ses
- `.wav` formatında temp klasörüne kaydedilir
- Otomatik transkribe edilmez (kullanıcı seçer)

### Transcription (Transkripsiyon)
- Ses → Metin dönüşümü
- Groq Cloud Whisper API kullanılır
- Türkçe dil desteği (`language="tr"`)

### Injection (Enjeksiyon)
- Transkribe metninin aktif pencereye yapıştırılması
- Clipboard yöntemi (Unicode desteği için)
- Kullanıcının kendi clipboard'i korunur

### History (Geçmiş)
- Oturum sırasında yapılan kayıtların listesi
- Bellekte tutulur (in-memory)
- Uygulama kapanınca silinir

---

## 🎨 Renk Paleti

| Renk | Hex | Kullanım |
|------|-----|----------|
| Turuncu | `#FF6B35` | Vurgu, butonlar, aktif öğeler |
| Koyu Gri | `#0c0c0c` | Ana arka plan |
| Cam Efekti | `#2a2a2e` | Pencere arka planı |
| Beyaz | `#ffffff` | Birincil metin |
| Gri | `#a0a0a0` | İkincil metin |
| Kırmızı | `#ff3b30` | Kayıt durdurma, uyarılar |

---

## 📝 Önemli Notlar

### Beep Sound Toggle
- Eskiden: Ayar değişince etkili olmuyordu
- Şimdi: `os.environ` güncelleniyor, hemen etkili olur

### Hotkey Değişikliği
- Eskiden: `Ctrl+Alt+Space`
- Şimdi: `Ctrl+Alt+K`
- Önceki hotkey'i kullananlar için: değişiklik!

### Auto-Transcription KALDIRILDI
- Eskiden: Kayıt biterse otomatik transkribe olurdu
- Şimdi: History'ye eklenir, kullanıcı manuel seçer
- Neden?: Kullanıcı birden fazla kayıt yapıp, seçip transkribe etmek istedi

### Window Behavior
- Eskiden: İki pencere (boş + settings)
- Şimdi: SettingsWindow ana penceredir
- Kapatınca: Tray'e küçülür (çalışmaya devam)

---

## 🐛 Bilinen Sorunlar ve Çözümleri

| Sorun | Çözüm |
|-------|--------|
| Beep toggle çalışmıyor | `os.environ` güncellendi (config.py) |
| History boş görünüyor | `CTkCheckBox` parametreleri düzeltildi |
| İkinci dosya transkribe olmuyor | Debug eklenmiş, test ediliyor |

---

## 📚 Ek Kaynaklar

- **Groq API**: https://console.groq.com/
- **CustomTkinter**: https://customtkinter.tomschmitt.xyz/
- **PyStray**: https://github.com/moses-palmer/pystray
- **Whisper**: https://github.com/openai/whisper
