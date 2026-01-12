# UI Modülleri - Kullanıcı Arayüzü Bileşenleri

Bu klasör, uygulamanın görsel arayüzünü oluşturan tüm bileşenleri içerir.

---

## `overlay.py` - Kayıt Durum Penceresi

**Amaç:** Kayıt sırasında görünen yüzen durumu göstergesi

**Sınıf:** `RecordingOverlay` (CTkToplevel)

**Özellikler:**
- Frameless pencere (`overrideredirect(True)`)
- Her zaman üstte (`attributes('-topmost', True)`)
- Hareketli mikrofon ikonu (pulse animasyonu)
- "Recording..." metni
- 5 adet animasyonlu dalga formu çubukları
- Cam/Akrilik tasarım

**Önemli Metotlar:**
- `show()` - Pencereyi gösterir (kayıt başladığında)
- `hide()` - Pencereyi gizler (kayıt durduğunda)

**Görsel Tasarım:**
- **Pencere:** ~250x80px, yuvarlatılmış köşeler
- **İkon:** Turuncu mikrofon (#FF6B35)
- **Animasyon:** 5 bar, height değişimi ile ses simülasyonu
- **Konum:** Ekranın ortasında belirir

**Kullanım:**
```python
overlay = RecordingOverlay(root_window)
overlay.show()   # Kayıt başladı
overlay.hide()   # Kayıt bitti
```

---

## `settings_window.py` - Ayarlar Penceresi

**Amaç:** Ana ayarlar ve kayıt geçmişi arayüzü

**Sınıf:** `SettingsWindow` (CTk - ana pencere)

**Önemli Bölümler:**

### 1. Header (Üst Kısım)
- Başlık: "GroqWhisper Settings"
- macOS tarzı kontrol noktaları (kırmızı, sarı, yeşil noktalar)
- Kırmızı nokta: Close → sistem tepsisine küçült
- Sarı nokta: Minimize
- Yeşil nokta: Maximize

### 2. Recording History (Kayıt Geçmişi) - EN ÜSTTE
- Kayıtlar listesi (checkbox ile seçim)
- Her kayıt için:
  - Dosya adı [Ready/Done]
  - Zaman damgası • Boyut
  - Transkribe edilmişse metin önizlemesi
- "Transcribe Selected" butonu
- "Delete Selected" butonu

### 3. Transcribe from File (Dosyadan Çevir)
- Dosya seçim butonu ("Browse")
- Dosya yolu giriş alanı
- "Transcribe File" butonu

### 4. API Key
- Maskeli giriş alanı (•••••••)
- Yanında anahtar ikonu (🔑)
- "gsk_..." placeholder

### 5. Input Device (Mikrofon Seçimi)
- Dropdown menü
- Sistemdeki tüm mikrofonları listeler

### 6. Activation Hotkey
- Salt okunur alan
- Gösterge: "Ctrl + Alt + K"

### 7. Preferences (Tercihler)
- "Play Beep Sound" toggle
- "Show Floating Overlay" toggle

### 8. Recording Button (Kayıt Butonu)
- Büyük, belirgin buton (60px yükseklik)
- "🎙 START RECORDING" / "⏹ STOP RECORDING"
- Kayıt sırasında kırmızı renk (#ff3b30)

### 9. Save Configuration (Kaydet Butonu)
- "Save Configuration" butonu
- Başarılı olduğunda "✓ Saved!" mesajı

**Pencere Özellikleri:**
- **Boyut:** 450x750 piksel
- **Scrollable:** İçerik taşarsa kaydırılabilir
- **Tasarım:** Koyu tema, cam efekti (#2a2a2e)

**Önemli Metotlar:**
```python
# Arayüz oluşturma
_create_header()           # Üst kısım
_create_history_view()      # Kayıt geçmişi (EN ÜST)
_create_file_upload()       # Dosya yükleme
_create_api_key_field()     # API key
_create_mic_dropdown()      # Mikrofon seçimi
_create_hotkey_field()      # Hotkey gösterimi
_create_toggles()           # Tercihler
_create_recording_button()  # Kayıt butonu
_create_save_button()       # Kaydet butonu

# İşlevsellik
_refresh_history()          # Geçmişi yenile
_transcribe_selected()      # Seçiliyi transkribe et
_delete_selected()         # Seçiliyi sil
_browse_file()              # Dosya seçme diyaloğu
_transcribe_file()          # Seçili dosyayı transkribe et
_toggle_recording()        # Kayıt başlat/durdur
_update_recording_button() # Buton durumunu güncelle
```

---

## `tray.py` - Sistem Tepsisi

**Amaç:** Uygulamayı arka planda çalıştırma

**Sınıf:** `SystemTray`

**Kütüphane:** `pystray` + `PIL` (Pillow)

**Özellikler:**
- Sistem tepsisi ikonu (turuncu mikrofon)
- Sağ tık menüsü:
  - "Restore Settings" - Ayarlar penceresini açar
  - "Quit" - Uygulamadan çıkar
- Daemon thread'de çalışır (engellemesiz)

**İkon Oluşturma:**
- Programatik olarak PIL ile oluşturulur
- 64x64 piksel
- Koyu arka plan (#2a2a2e)
- Turuncu mikrofon şekli (#FF6B35)

**Önemli Metotlar:**
- `run()` - Tepsisini başlatır
- `stop()` - Tepsisini durdurur
- `update_tooltip(text)` - İpucu metnini günceller (örn: "Recording...")

**Menü Yapısı:**
```python
menu = pystray.Menu(
    pystray.MenuItem("Restore Settings", on_restore),
    pystray.MenuItem("Quit", on_quit)
)
```

---

## Renk Paleti (CSS → CTk)

```python
BG_COLOR = "#0c0c0c"              # Derin arka plan
GLASS_BG = ("#2a2a2e", "#323238")  # Cam efekti
ACCENT_COLOR = "#FF6B35"          # Turuncu vurgu
TEXT_PRIMARY = "#ffffff"           # Beyaz metin
TEXT_SECONDARY = "#a0a0a0"        # Gri metin
INPUT_BG = ("#1a1a1a", "#222222")  # Giriş alanı arka planı
DANGER_COLOR = "#ff3b30"          # Kırmızı (kayıt durdurma)
```

---

## Dosya Yapısı

```
src/ui/
├── overlay.py           # Kayıt durumu göstergesi (yüzen pencere)
├── settings_window.py   # Ana ayarlar penceresi (CTk main window)
└── tray.py              # Sistem tepsisi entegrasyonu
```

---

## Bağımlılıklar

```
ui/
├── overlay.py → customtkinter, math
├── settings_window.py → customtkinter, tkinter.filedialog, pathlib
└── tray.py → pystray, PIL (Image, ImageDraw)
```

---

## UI Akış Diagramı

```
┌─────────────────────────────────────────┐
│         GroqWhisper Settings              │
├─────────────────────────────────────────┤
│ [1] Recording History (3)     ← EN ÜST   │
│     ☑ recording_xxx.wav [Ready]         │
│     ☐ recording_yyy.wav [Done]          │
│     "merhaba..."                        │
│     [Transcribe Selected] [Delete]       │
├─────────────────────────────────────────┤
│ [2] Transcribe from File                │
│     [Select File...]        🔊          │
│     [Transcribe File]                   │
├─────────────────────────────────────────┤
│ [3] API Key: [••••••••] 🔑              │
│ [4] Input Device: [Dropdown ▼]           │
│ [5] Hotkey: Ctrl + Alt + K       ⌨      │
│ [6] ☑ Play Beep Sound                    │
│ [7] ☑ Show Floating Overlay             │
│ [8] 🎙 START RECORDING                  │
│ [9] [Save Configuration]                 │
└─────────────────────────────────────────┘
```
