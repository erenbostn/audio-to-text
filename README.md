# GroqWhisper Desktop

Windows masaüstü uygulaması - ses kaydedin ve Groq'un Whisper API'si ile anında metne çevirin.

## Özellikler

- 🎙️ **Global Hotkey ile Kayıt**: `Ctrl+Alt+K` tuş kombinasyonu ile ses kaydedin
- ⚡ **Anında Transkripsiyon**: Groq Whisper API ile hızlı ve doğru metne çeviri
- 📋 **Otomatik Metin Ekme**: Transkript metni otomatik olarak imleç konumuna ekler
- 📁 **Dosya Yükleme**: Harici ses dosyalarını transkript edin
- 📜 **Kayıt Geçmişi**: Tüm kayıtlar geçmişte saklanır, seçili olarak transkript edin
- 🌍 **Çoklu Dil Desteği**: Türkçe, İngilizce, Almanca, Fransızca, İspanyolca, İtalyanca ve otomatik algılama
- 💾 **İndirme ve Kopyalama**: Transkriptleri .txt dosyası olarak indirin veya kopyalayın

## Görünüm

```
┌─────────────────────────────────────────┐
│ GroqWhisper Settings                    │
├─────────────────────────────────────────┤
│ Recording History (2)                   │
│ ☐ 📁 speech.wav          [Done]  5MB   │
│ ☐ 🎙 recording_123.wav   [Ready] 2MB   │
├─────────────────────────────────────────┤
│ Transcription:                          │
│ ┌─────────────────────────────────────┐ │
│ │ Kaydedilen sesin metni burada      │ │
│ │ görünür...                          │ │
│ └─────────────────────────────────────┘ │
│ [Copy]           [Download .txt]        │
├─────────────────────────────────────────┤
│ [🎙 START RECORDING]                   │
└─────────────────────────────────────────┘
```

## Gereksinimler

- **Windows** 10 veya üzeri
- **Python** 3.10 veya üzeri

## Kurulum

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/eren/audio_to_text.git
cd audio_to_text
```

### 2. Sanal Ortam Oluşturun (Önerilen)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

## Yapılandırma

### 1. Groq API Key Alın

1. [Groq Console](https://console.groq.com/keys)'a gidin
2. Ücretsiz API key oluşturun

### 2. .env Dosyası Oluşturun

```bash
# .env.example dosyasını kopyalayın
copy .env.example .env
```

### 3. .env Dosyasını Düzenleyin

```
GROQ_API_KEY=groq_xxxxxxxxxxxxxxxxxxxxxxxx
TRANSCRIPTION_LANGUAGE=tr
PLAY_BEEP_SOUND=true
SHOW_OVERLAY=true
```

## Kullanım

### Uygulamayı Başlatın

```bash
python src/main.py
```

### Ses Kaydı

1. Uygulamayı başlatın
2. `Ctrl+Alt+K` tuşlarına basın
3. Konuşun (kayıt başlar)
4. Tekrar `Ctrl+Alt+K` basın (kayıt durur)
5. Transkript otomatik olarak yapılır ve metin eklenir

### Dosyadan Transkripsiyon

1. Ayarlar penceresinde "Transcribe from File" bölümüne gidin
2. "Select File..." ile ses dosyasını seçin
3. "Transcribe File" butonuna tıklayın
4. Sonuç görünür, kopyalayın veya indirin

### Kayıt Geçmişi

1. Ayarlar penceresinde "Recording History" bölümünü görün
2. Kayıtlar listelenir:
   - 📁 = Dosyadan yükleme
   - 🎙 = Mikrofon kaydı
3. İşaretleyip "Transcribe Selected" ile transkript edin
4. Seçili kaydın tam metnini görün, kopyalayın veya indirin

## Desteklenen Formatlar

- **Kayıt:** `.wav` (geçici dosya)
- **Dosya Yükleme:** `.wav`, `.mp3`, `.ogg`, `.flac`

## Desteklenen Diller

- Türkçe - Türkçe
- English
- Deutsch
- Français
- Español
- Italiano
- Auto-detect (Otomatik algılama)

## Proje Yapısı

```
audio_to_text/
├── src/
│   ├── core/
│   │   ├── recorder.py         # Ses kaydı
│   │   ├── transcriber.py      # Groq API transkripsiyon
│   │   ├── input_simulator.py  # Metin ekme
│   │   └── history_manager.py  # Kayıt geçmişi
│   ├── ui/
│   │   ├── overlay.py          # Kayıt göstergesi
│   │   ├── settings_window.py  # Ayarlar penceresi
│   │   └── tray.py             # Sistem tepsisi
│   ├── models/
│   │   └── recording.py        # Kayıt veri modeli
│   ├── utils/
│   │   └── sound_feedback.py   # Beep sesleri
│   ├── config.py               # Yapılandırma yönetimi
│   └── main.py                 # Ana giriş noktası
├── docs/                       # Proje dokümantasyonu
├── .env.example                # Ortam değişkenleri şablonu
└── requirements.txt            # Python bağımlılıkları
```

## Lisans

MIT License

## Katkıda Bulunma

1. Depoyu fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inize push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## Sorunlar

Sorun bildirmek için [Issues](https://github.com/eren/audio_to_text/issues) sayfasını kullanın.
