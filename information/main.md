# Config & Main - Yapılandırma ve Ana Uygulama

Bu bölüm, uygulamanın başlatılmasını ve yapılandırmasını yöneten dosyaları açıklar.

---

## `config.py` - Yapılandırma Yöneticisi

**Amaç:** .env dosyasından ayarları okumak ve yazmak

**Sınıf:** `Config`

**Önemli Metotlar:**

| Metot | Açıklama | Dönüş Tipi |
|-------|----------|------------|
| `get_api_key()` | Groq API key'ini döndürür | `str \| None` |
| `save_api_key(key)` | API key'i .env'e yazar | `void` |
| `get_sample_rate()` | Örnekleme oranını döndürür | `int` (varsayılan: 16000) |
| `get_channels()` | Kanal sayısını döndürür | `int` (varsayılan: 1) |
| `get_hotkey()` | Hotkey kombinasyonunu döndürür | `str` |
| `show_overlay()` | Overlay gösterim tercihi | `bool` |
| `play_beep()` | Beep sesi tercihi | `bool` |
| `reload_env()` | .env dosyasını yeniden yükler | `void` |
| `save_beep_setting(enabled)` | Beep ayarını kaydeder | `void` |
| `save_overlay_setting(enabled)` | Overlay ayarını kaydeder | `void` |

**.env Dosyası Yapısı:**
```bash
GROQ_API_KEY=gsk_...
PLAY_BEEP_SOUND=true
SHOW_OVERLAY=true
RECORDING_SAMPLE_RATE=16000
RECORDING_CHANNELS=1
DEFAULT_HOTKEY=<ctrl>+<alt>+<space>
```

**Önemli Değişiklik (v1.1):**
- Önceden: Ayarlar değiştiğinde `os.environ` güncellenmiyordu
- Şimdi: `save_beep_setting()` ve `save_overlay_setting()` hem .env'e yazar hem `os.environ`'ı günceller
- Bu sayede toggle'lar hemen etkili olur

**Kullanım:**
```python
config = Config()

# Okuma
api_key = config.get_api_key()
play_beep = config.play_beep()

# Yazma
config.save_api_key("gsk_abc123...")
config.save_beep_setting(False)  # Hem .env'e yazar, hem os.environ'ı günceller
```

---

## `main.py` - Ana Uygulama

**Amaç:** Tüm bileşenleri bir araya getiren ana orkestratör

**Sınıf:** `GroqWhisperApp`

**Yaşam Döngüsü:**

```
1. Başlatma (__init__)
   ├─→ CustomTkinter başlatma
   ├─→ Config yükleme
   ├─→ Core modülleri (recorder, transcriber, injector)
   ├─→ History manager oluştur
   ├─→ SettingsWindow AÇ (ana pencere)
   ├─→ Overlay oluştur (başlangıçta gizli)
   └─→ Hotkey listener başlat

2. Kayıt Akışı (_on_hotkey_pressed)
   ├─→ _start_recording()
   │   ├─→ Beep sesi çal (1000Hz)
   │   ├─→ Overlay göster
   │   ├─→ Kaydı başlat
   │   └─→ Tray tooltip: "Recording..."
   │
   └─→ _stop_recording()
       ├─→ Kaydı durdur
       ├─→ Overlay gizle
       ├─→ Beep sesi çal (700Hz)
       ├─→ Kaydı HISTORY'ye ekle (otomatik transkribe ETMEZ)
       └─→ UI'yi yenile

3. Kapatma (shutdown)
   ├─→ Hotkey listener'ı durdur
   ├─→ Tray ikonunu durdur
   ├─→ Temp dosyalarını sil
   └─→ Uygulamadan çık (os._exit(0))
```

**Önemli Metotlar:**

| Metot | Açıklama |
|-------|----------|
| `_setup_components()` | Core modülleri başlatır (UI'den önce) |
| `_setup_remaining_components()` | UI bileşenlerini başlatır (root'dan sonra) |
| `_setup_hotkeys()` | Global hotkey listener'ı başlatır |
| `_on_hotkey_pressed()` | Hotkey basıldığında çağrılır |
| `_start_recording()` | Kaydı başlatır |
| `_stop_recording()` | Kaydı durdurur, history'ye ekler |
| `_show_settings()` | Ayarlar penceresini gösterir |
| `_on_settings_close()` | Ayarlar penceresi kapanınca (minimize to tray) |
| `run()` | Ana döngüyü başlatır |
| `shutdown()` | Temiz kapanış |

**Global Hotkey'ler:**
- `Ctrl+Alt+K`: Kayıt başlat/durdur
- `Ctrl+Alt+Q`: Uygulamadan çık

**Threading Yapısı:**
```
Main Thread (UI)
├─→ SettingsWindow (CTk main loop)
└─→ RecordingOverlay (CTkToplevel)

Daemon Threads
├─→ Hotkey Listener (pynput)
└─→ System Tray Icon (pystray)

Worker Threads (recording sırasında)
└─→ Audio Recorder (sounddevice callback)
```

---

## Uygulama Başlatma Akışı

```
python src/main.py
        │
        ↓
┌─────────────────────────────────┐
│ GroqWhisperApp.__init__()       │
├─────────────────────────────────┤
│ 1. CustomTkinter başlat         │
│ 2. Config yükle                 │
│ 3. Core modülleri oluştur:      │
│    - AudioRecorder              │
│    - GroqTranscriber            │
│    - TextInjector               │
│    - HistoryManager             │
│    - SoundFeedback              │
│    - SystemTray                 │
│ 4. SettingsWindow AÇ            │
│    (Bu ANA penceredir!)         │
│ 5. Overlay oluştur (gizli)      │
│ 6. Hotkey'leri başlat           │
└─────────────────────────────────┘
        │
        ↓
┌─────────────────────────────────┐
│ SettingsWindow Görünür          │
│ (History en üstte)               │
│                                  │
│ [1] Recording History            │
│ [2] Transcribe from File        │
│ [3] API Key                      │
│ [4] Microphone                   │
│ [5] Hotkey                       │
│ [6] Toggles                      │
│ [7] Recording Button            │
│ [8] Save Config                  │
└─────────────────────────────────┘
        │
        ↓
Ctrl+Alt+K (hotkey)
        │
        ↓
┌─────────────────────────────────┐
│ _on_hotkey_pressed()            │
├─────────────────────────────────┤
│ IF recording:                   │
│   → _stop_recording()           │
│ ELSE:                           │
│   → _start_recording()          │
└─────────────────────────────────┘
```

---

## Sinyal Yönetimi

**Graceful Shutdown:**
```python
# SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, handler)

# SIGTERM (kill komutu)
signal.signal(signal.SIGTERM, handler)

# Shutdown sequence:
1. Hotkey listener.stop()
2. SystemTray.stop()
3. AudioRecorder.cleanup_temp_files()
4. root.quit()
5. os._exit(0)  # Zorla çık (garanti)
```

---

## Dosya Yapısı

```
src/
├── config.py         # .env yönetimi
└── main.py           # Ana uygulama döngüsü
```

---

## Önemli Sabitler

```python
# main.py
GroqWhisperApp._running = False    # Sınıf değişkeni (running state)
GroqWhisperApp._shutdown_flag = False  # Kapanma bayrağı

# Hotkey format (pynput)
'<ctrl>+<alt>+k'   # Doğru
'Ctrl+Alt+K'       # Yanlış!
```

---

## Hata Ayıklama İpuçları

**Sorun:** Pencere açılmıyor
**Çözüm:** `root.withdraw()`'i kaldır, SettingsWindow ana pencere olsun

**Sorun:** Hotkey çalışmıyor
**Çözüm:** Format kontrolü - modifiers `< >` içinde, key olmadan

**Sorun:** Kapanmıyor
**Çözüm:** `os._exit(0)` kullan - tüm thread'leri zorla killer
