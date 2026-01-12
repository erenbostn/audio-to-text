# Utils - Yardımcı Fonksiyonlar

Bu klasör, uygulama için yardımcı ve util fonksiyonları içerir.

---

## `sound_feedback.py` - Ses Geri Bildirimi

**Amaç:** Kayıt başlama/durdurma sırasında sesli geri bildirim

**Sınıf:** `SoundFeedback`

**Sabitler:**
```python
START_BEEP_FREQ = 1000    # Başlangıç bip frekansı (Hz)
START_BEEP_DURATION = 200  # Başlangıç bip süresi (ms)
STOP_BEEP_FREQ = 700      # Bitiş bip frekansı (Hz)
STOP_BEEP_DURATION = 200   # Bitiş bip süresi (ms)
```

**Önemli Metotlar:**

| Metot | Açıklama |
|-------|----------|
| `play_start_beep()` | Kayıt başladığında 1000Hz bip |
| `play_stop_beep()` | Kayıt bittiğinde 700Hz bip |

**Tasarım Deseni:**
- Constructor'a bir callable (`enabled_check`) alır
- Her çalma öncesi kontrol eder: `if self._enabled():`
- Bu sayede toggle anında çalışmaz

**Platform:**
- Windows only (`winsound`)
- Linux/macOS'ta sessizce geçer (try/except ile)

**Kullanım:**
```python
# Config'den bir callable oluştur
sound = SoundFeedback(config.play_beep)

# Kayıt başlarken
sound.play_start_beep()  # → BİP! (1000Hz)

# Kayıt biterken
sound.play_stop_beep()   # → BİP! (700Hz)
```

**Çalışma Mantığı:**
```python
def play_start_beep(self):
    # 1. Toggle kontrolü
    if not self._enabled():
        return  # Beep kapalıysa, hiçbir şey yapma

    # 2. Platform kontrolü
    if sys.platform != 'win32':
        return  # Sadece Windows

    # 3. Bip çal
    try:
        import winsound
        winsound.Beep(self.START_BEEP_FREQ, self.START_BEEP_DURATION)
    except Exception:
        pass  # Hata olursa sessizce geç
```

---

## Dosya Yapısı

```
src/utils/
└── sound_feedback.py    # Winsound bip sesleri
```

---

## Bağımlılık Grafiği

```
utils/
└── sound_feedback.py
    ├─→ sys (platform check)
    └─→ winsound (Windows only)

sound_feedback.py
    └─→ Config (enabled_check callable)
```

---

## Gelecek Eklentiler

İleriye eklenebilecek util modülleri:

### `audio_utils.py` - Ses Araçları
```python
def get_duration(file_path) -> float:
    """Ses dosyasının süresini döndürür (saniye)"""

def convert_to_wav(source_path) -> str:
    """Herhangi bir formatı .wav'a çevirir"""

def get_audio_info(file_path) -> dict:
    """Sample rate, channels, duration döndürür"""
```

### `file_utils.py` - Dosya Araçları
```python
def ensure_temp_dir() -> Path:
    """Temp klasörünün varlığını garanti eder"""

def clean_old_files(max_age_hours: int = 24):
    """X saatten eski dosyaları temizler"""

def get_disk_usage() -> dict:
    """Disk kullanım istatistiklerini döndürür"""
```

### `validation.py` - Doğrulama
```python
def validate_api_key(api_key: str) -> bool:
    """API key formatını doğrular"""

def validate_audio_file(file_path: str) -> bool:
    """Dosyanın geçerli ses dosyası olduğunu kontrol eder"""

def validate_audio_device(device_id: int) -> bool:
    """Ses cihazının kullanılabilir olduğunu kontrol eder"""
```
