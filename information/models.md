# Models - Veri Modelleri

Bu klasör, uygulama içinde kullanılan veri yapılarını ve modellerini içerir.

---

## `recording.py` - Kayıt Modeli

**Amaç:** Bir ses kaydının tüm bilgilerini tutan veri sınıfı

**Sınıf:** `Recording` (dataclass)

**Özellikler:**

```python
@dataclass
class Recording:
    id: str                    # Benzersiz kimlik (timestamp)
    filepath: str              .wav dosyasının tam yolu
    created_at: datetime        # Oluşturulma zamanı
    transcribed: bool = False  # Transkribe edildi mi?
    transcript: str | None = None  # Transkribe metin
```

**Property'ler (Hesaplanan Alanlar):**

| Property | Açıklama | Dönüş Tipi |
|----------|----------|-------------|
| `filename` | Dosya adı (path olmadan) | `str` |
| `file_size` | Dosya boyutu (byte) | `int` |
| `file_size_mb` | Dosya boyutu (megabayt) | `float` |
| `file_size_kb` | Dosya boyutu (kilobayt) | `float` |
| `transcript_preview` | Transkript önizlemesi (kısaltılmış) | `str` |

**Kullanım Örneği:**
```python
from models.recording import Recording
from datetime import datetime

# Yeni kayıt oluştur
recording = Recording(
    id="1736659200000",
    filepath="C:/Users/eren/Desktop/audio_to_text/temp/recording_1736659200000.wav",
    created_at=datetime.now(),
    transcribed=False,
    transcript=None
)

# Bilgilere eriş
print(recording.filename)           # "recording_1736659200000.wav"
print(recording.file_size_kb)       # 45.2
print(recording.transcript_preview(50))  # "merhaba nasılsın, bugün nasılsın..."

# Transkripsiyon tamamlandı
recording.transcribed = True
recording.transcript = "merhaba nasılsın"
```

**Transcript Preview:**
Transkript metni çok uzunsa, önizleme otomatik kısaltılır:
- `max_length=50` (varsayılan)
- 50 karakterden uzunsa → `"..."` eklenir

---

## Veri Akışı

```
Kayıt Oluşturma:
┌─────────────────┐
│ AudioRecorder   │
│ .stop_recording()│
└────────┬────────┘
         │ filepath
         ↓
┌─────────────────┐
│ HistoryManager  │
│ .add_recording()│
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Recording       │
│ (dataclass)     │
│ - id            │
│ - filepath      │
│ - created_at    │
│ - transcribed   │
│ - transcript    │
└─────────────────┘
         │
         ↓ (kullanıcı seçimi)
┌─────────────────┐
│ GroqTranscriber │
│ .transcribe()   │
└────────┬────────┘
         │ text
         ↓
┌─────────────────┐
│ Recording       │
│ transcript = text│
│ transcribed=True │
└─────────────────┘
```

---

## Dosya Yapısı

```
src/models/
├── __init__.py      # Paket başlatıcı
└── recording.py     # Recording dataclass
```

---

## Neden Dataclass?

**Avantajları:**
- Otomatik `__init__` metodu
- Otomatik `__repr__` metodu (debug için)
- Tip hinting desteği
- Değiştirilemez (immutable) yapılabilir (`frozen=True`)

**Type Hint'ler:**
```python
id: str                              # Zorunlu
filepath: str                        # Zorunlu
created_at: datetime                 # Zorunlu
transcribed: bool = False            # Opsiyonel (varsayılan)
transcript: str | None = None       # Opsiyonel (varsayılan)
```

---

## İlişkiler

```
Recording ile İlişkili:

1. HistoryManager
   → _recordings: dict[str, Recording]
   → add_recording(filepath) → Recording
   → get_recings() → list[Recording]

2. SettingsWindow
   → _create_history_item(recording)
   → recording.filename, recording.file_size_kb, etc.
```

---

## Future Extensions

İleriide eklenebilecek özellikler:

```python
@dataclass
class Recording:
    # Mevcut alanlar...

    # Potansiyel yeni alanlar:
    duration: float = 0.0           # Kayıt süresi (saniye)
    language: str = "tr"            # Transkripsiyon dili
    confidence: float = 0.0         # Güven skoru (0-1)
    tags: list[str] = None          # Kullanıcı etiketleri
    starred: bool = False           # Favorilendi mi?
```
