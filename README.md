# 🎙️ GroqWhisper Desktop

**Windows masaüstü uygulaması** - Ses kaydedin veya dosya yükleyin, Groq'un Whisper API'si ile anında metne çevirin.

![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Gereksinimler](#-gereksinimler)
- [Kurulum](#-kurulum)
- [Yapılandırma](#-yapılandırma)
- [Kullanım](#-kullanım)
- [Klavye Kısayolları](#-klavye-kısayolları)
- [Desteklenen Formatlar](#-desteklenen-formatlar)
- [Sorun Giderme](#-sorun-giderme)
- [Katkıda Bulunma](#-katkıda-bulunma)

---

## ✨ Özellikler

| Özellik | Açıklama |
|---------|----------|
| 🎙️ **Global Hotkey** | `Ctrl+Alt+K` ile herhangi bir uygulamadan ses kaydı başlatın/durdurun |
| ⚡ **Anında Transkripsiyon** | Groq Whisper API ile hızlı ve doğru metne çeviri |
| 📋 **Otomatik Yapıştır** | Transkript otomatik olarak panoya kopyalanır ve aktif uygulamaya yapıştırılır |
| 📁 **Dosya Yükleme** | Harici ses dosyalarını (wav, mp3, m4a, ogg, flac) transkript edin |
| ✂️ **Uzun Dosya Parçalama** | 10 dakikadan uzun dosyalar otomatik olarak 4 dakikalık parçalara bölünür |
| 📜 **Kayıt Geçmişi** | Tüm kayıtlar listelenir, seçilebilir, birleştirilebilir |
| ✏️ **Düzenleme Modu** | Kilit açma ile transkript metinleri düzenlenebilir |
| 🌍 **Çoklu Dil Desteği** | Türkçe, İngilizce, Almanca, Fransızca, İspanyolca, İtalyanca |
| 🔄 **İngilizce'ye Çeviri** | Konuşmayı doğrudan İngilizce'ye çevirin |
| 💾 **İndirme ve Kopyalama** | Transkriptleri .txt dosyası olarak kaydedin |
| 🔊 **Ses Geri Bildirimi** | Kayıt başlangıç/bitiş sesleri |

---

## 🖼️ Ekran Görüntüleri

```
┌─────────────────────────────────────────────────────────┐
│  GroqWhisper                             Ctrl+Alt+K    │
├─────────────────────────────────────────────────────────┤
│  [🔴 Start Recording]        [📁 Upload File]          │
│          00:00                                          │
├─────────────────────────────────────────────────────────┤
│  Configuration                                          │
│  ─────────────────────────────────────────────────────  │
│  Groq API Key: [••••••••••••••••••] [Save]             │
│  Microphone:   [Default System Microphone ▼]           │
│  Language:     [Turkish - Türkçe ▼]                    │
│                                                         │
│  ┌──────┐ ┌──────────┐ ┌────────────┐ ┌────────┐       │
│  │Sound │ │Auto-Paste│ │Translate EN│ │ Locked │       │
│  │  ☑   │ │    ☑     │ │     ☐      │ │   🔒   │       │
│  └──────┘ └──────────┘ └────────────┘ └────────┘       │
├─────────────────────────────────────────────────────────┤
│  History                                    Clear All   │
│  ─────────────────────────────────────────────────────  │
│  [Merge] [Delete Selected]                              │
│                                                         │
│  ☐ [Parça 1] 14:05:23  Copy  Download                  │
│    "Merhaba, bugün sizlere önemli bir konuyu..."       │
│                                                         │
│  ☐ [Parça 2] 14:05:24  Copy  Download                  │
│    "...anlatmak istiyorum. Bu konu hakkında..."        │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Gereksinimler

- **İşletim Sistemi:** Windows 10 veya üzeri
- **Python:** 3.10 veya üzeri
- **Groq API Key:** Ücretsiz olarak alınabilir

---

## 🚀 Kurulum

### Adım 1: Projeyi İndirin

```bash
git clone https://github.com/eren/audio_to_text.git
cd audio_to_text
```

### Adım 2: Sanal Ortam Oluşturun (Önerilen)

```bash
# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktifleştir (Windows)
venv\Scripts\activate
```

> 💡 **İpucu:** Sanal ortam kullanmak, projenin bağımlılıklarını sistem Python'undan izole eder.

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

Bu komut aşağıdaki paketleri yükleyecektir:
- `pywebview` - Modern UI framework
- `sounddevice`, `numpy`, `soundfile` - Ses kaydı
- `mutagen` - Ses dosyası meta verileri (m4a desteği için)
- `groq` - Groq API client
- `pystray`, `Pillow` - Sistem tepsisi
- `pynput` - Global hotkey
- `pyautogui`, `pyperclip` - Otomatik yapıştırma

---

## ⚙️ Yapılandırma

### Groq API Key Alma (Ücretsiz)

1. [Groq Console](https://console.groq.com/keys) adresine gidin
2. Ücretsiz hesap oluşturun veya giriş yapın
3. "Create API Key" butonuna tıklayın
4. Oluşturulan key'i kopyalayın (`gsk_...` ile başlar)

### .env Dosyası Oluşturma

**Yöntem 1: Örnek dosyadan kopyalama**

```bash
copy .env.example .env
```

**Yöntem 2: Manuel oluşturma**

Proje kök dizininde `.env` adlı bir dosya oluşturun:

```env
# Groq API Key (zorunlu)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Dil ayarı (varsayılan: tr)
# Seçenekler: tr, en, de, fr, es, it, auto
TRANSCRIPTION_LANGUAGE=tr

# Ses geri bildirimi (varsayılan: true)
PLAY_BEEP_SOUND=true

# Otomatik yapıştır - Ctrl+V (varsayılan: true)
AUTO_PASTE=true

# İngilizce'ye çevir (varsayılan: false)
TRANSLATE_TO_EN=false
```

> ⚠️ **Önemli:** `.env` dosyası gizli kalmalıdır. Bu dosya `.gitignore` tarafından versiyon kontrolünden hariç tutulmuştur.

---

## 🎯 Kullanım

### Uygulamayı Başlatma

```bash
python src/main.py
```

Başarılı başlatma sonrası konsolda şu mesajı göreceksiniz:
```
Hotkeys registered: <ctrl>+<alt>+k
GroqWhisper Desktop - Starting Webview...
System tray icon started.
```

### Ses Kaydı ile Transkripsiyon

1. **Kayıt Başlat:** `Ctrl+Alt+K` tuşlarına basın veya "Start Recording" butonuna tıklayın
2. **Konuşun:** Mikrofona konuşun (kayıt süresi ekranda görünür)
3. **Kayıt Durdur:** Tekrar `Ctrl+Alt+K` basın veya butona tıklayın
4. **Otomatik İşlem:**
   - Ses dosyası kaydedilir
   - Groq API'ye gönderilir
   - Transkript panoya kopyalanır
   - Auto-Paste açıksa otomatik yapıştırılır

### Dosyadan Transkripsiyon

1. "Upload File" butonuna tıklayın
2. Ses dosyasını seçin (.wav, .mp3, .m4a, .ogg, .flac)
3. **Kısa dosyalar (<10 dakika):** Otomatik olarak transkript edilir
4. **Uzun dosyalar (>10 dakika):** Parçalama onayı istenir

### 🔀 Uzun Dosya İşleme (Otomatik Parçalama)

Groq API'nin 25MB dosya sınırı nedeniyle uzun ses dosyaları otomatik olarak parçalanır:

1. Uzun dosya yüklendiğinde "Dosya Parçalanmalı" modalı açılır
2. "Parçala ve Transcribe Et" butonuna tıklayın
3. Dosya **4 dakikalık** parçalara bölünür (10 saniye overlap ile)
4. Her parça sırayla transkript edilir (ilerleme çubuğu gösterilir)
5. Parçalar History bölümünde "Parça 1", "Parça 2" vb. etiketleriyle görünür
6. İstediğiniz parçaları seçip "Merge" butonu ile birleştirebilirsiniz

### 📝 Kayıt Geçmişi Kullanımı

| İşlem | Açıklama |
|-------|----------|
| **Seçim** | Kayıtların yanındaki checkbox'ları işaretleyin |
| **Sıra Numarası** | Seçim sıranız turuncu badge ile gösterilir (birleştirme sırası için önemli) |
| **Birleştirme** | Seçili kayıtları "Merge" butonu ile birleştirin |
| **Kopyalama** | "Copy" butonu ile panoya kopyalayın |
| **İndirme** | "Download" ile .txt dosyası olarak kaydedin |
| **Silme** | "Delete Selected" ile seçilenleri silin |

### ✏️ Düzenleme Modu

Transkript metinlerini düzenlemek için:

1. Ayarlar bölümündeki **"Locked"** butonuna tıklayın
2. Buton **"Edit ON"** olarak değişir (turuncu renk)
3. Artık History'deki metinlere tıklayıp düzenleyebilirsiniz
4. Düzenlemeler otomatik kaydedilir (focus değiştiğinde)
5. Tekrar "Edit ON" butonuna tıklayarak düzenleme modunu kapatın

---

## ⌨️ Klavye Kısayolları

| Kısayol | İşlev |
|---------|-------|
| `Ctrl+Alt+K` | Kayıt başlat/durdur (Global - her uygulamada çalışır) |

---

## 📁 Desteklenen Formatlar

### Giriş Formatları
| Format | Uzantı | Açıklama |
|--------|--------|----------|
| WAV | `.wav` | Sıkıştırılmamış ses |
| MP3 | `.mp3` | Sıkıştırılmış ses |
| M4A | `.m4a` | Apple ses formatı |
| OGG | `.ogg` | Vorbis codec |
| FLAC | `.flac` | Kayıpsız sıkıştırma |

### Çıkış Formatları
- `.txt` - UTF-8 metin dosyası

### Desteklenen Diller

| Kod | Dil | Kod | Dil |
|-----|-----|-----|-----|
| `tr` | Türkçe | `fr` | Français |
| `en` | English | `es` | Español |
| `de` | Deutsch | `it` | Italiano |
| `auto` | Otomatik Algılama | | |

---

## ⚙️ Ayarlar Açıklaması

| Toggle | Açıklama |
|--------|----------|
| **Sound** | Kayıt başlangıç/bitiş bip sesleri |
| **Auto-Paste** | Transkript sonrası otomatik Ctrl+V (aktif uygulamaya yapıştırır) |
| **Translate EN** | Transkripsiyon yerine İngilizce'ye çeviri yapar |
| **Locked / Edit ON** | Metin düzenleme modunu açar/kapatır |

---

## 🔧 Sorun Giderme

### "GROQ_API_KEY not found" hatası

**Çözüm:** `.env` dosyasını oluşturun ve API key'inizi ekleyin.

### Mikrofon algılanmıyor

**Çözümler:**
1. Windows Ses Ayarları'ndan mikrofonun etkin olduğunu kontrol edin
2. Uygulamayı yönetici olarak çalıştırın
3. Configuration bölümünden doğru mikrofonu seçin

### Kayıt başlamıyor

**Çözümler:**
1. Başka bir uygulama mikrofonu kullanıyor olabilir - kapatın
2. `Ctrl+Alt+K` başka bir uygulama tarafından kullanılıyor olabilir

### Transkripsiyon başarısız

**Çözümler:**
1. İnternet bağlantınızı kontrol edin
2. API key'in geçerli olduğunu doğrulayın (`gsk_` ile başlamalı)
3. Dosya boyutunun 25MB'ı aşmadığından emin olun (uzun dosyalar için parçalama kullanın)

### Pencere görünmüyor

**Çözümler:**
1. Sistem tepsisinde (sağ alt köşe) GroqWhisper ikonuna çift tıklayın
2. Görevi sonlandırıp tekrar başlatın

### Python veya pip bulunamıyor

**Çözümler:**
1. Python'un PATH'e eklendiğinden emin olun
2. Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin
3. Terminali yeniden başlatın

### Uzun dosya parçalanmıyor

**Çözümler:**
1. `soundfile` ve `mutagen` paketlerinin yüklü olduğunu kontrol edin
2. Desteklenen formatlarda dosya kullandığınızdan emin olun

---

## 📂 Proje Yapısı

```
audio_to_text/
├── src/
│   ├── core/
│   │   ├── api.py             # Python ↔ JS köprüsü
│   │   ├── recorder.py        # Ses kaydı modülü
│   │   ├── transcriber.py     # Groq API transkripsiyon
│   │   ├── audio_splitter.py  # Uzun dosya parçalama (4dk chunks)
│   │   ├── history_manager.py # Kayıt geçmişi yönetimi
│   │   └── input_simulator.py # Otomatik yapıştırma
│   ├── ui/
│   │   ├── index.html         # Ana arayüz (HTML/JS/Tailwind)
│   │   └── tray.py            # Sistem tepsisi
│   ├── models/
│   │   └── recording.py       # Veri modeli
│   ├── utils/
│   │   └── sound_feedback.py  # Ses geri bildirimi
│   ├── config.py              # Yapılandırma yönetimi
│   └── main.py                # Ana giriş noktası
├── docs/                      # Proje dokümantasyonu
├── temp/                      # Geçici ses dosyaları (otomatik oluşturulur)
├── .env.example               # Örnek yapılandırma dosyası
├── .gitignore                 # Git hariç tutulanlar
├── requirements.txt           # Python bağımlılıkları
└── README.md                  # Bu dosya
```

---

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inize push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

## 🐛 Sorunlar ve Öneriler

Sorun bildirmek veya öneride bulunmak için [Issues](https://github.com/eren/audio_to_text/issues) sayfasını kullanın.

---

## 🙏 Teşekkürler

- [Groq](https://groq.com/) - Hızlı Whisper API
- [PyWebview](https://pywebview.flowrl.com/) - Modern Python GUI
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
