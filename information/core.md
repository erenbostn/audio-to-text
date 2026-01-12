# Core Modüller - Çekirdek Fonksiyonlar

Bu klasör, uygulamanın ana işlevselliğini sağlayan modülleri içerir.

---

## `recorder.py` - Ses Kaydedici

**Amaç:** Mikrofondan ses yakalama ve .wav dosyası olarak kaydetme

**Sınıf:** `AudioRecorder`

**Önemli Metotlar:**
- `start_recording()` - Kaydı başlatır (engellemesiz thread'de çalışır)
- `stop_recording()` - Kaydı durdurur ve dosya yolunu döndürür
- `cleanup_temp_files()` - Temp klasöründeki tüm kayıtları siler

**Teknik Detaylar:**
- **Kütüphane:** `sounddevice` + `numpy`
- **Çıktı Formatı:** `.wav` dosyası (16-bit PCM, mono/stereo)
- **Depolama:** `project_root/temp/recording_{timestamp}.wav`
- **Sample Rate:** 16000 Hz (Groq Whisper için optimal)
- **Threading:** Kayıt sırasında UI'yi blokelamaz

**Kullanım Örneği:**
```python
recorder = AudioRecorder(sample_rate=16000, channels=1)
recorder.start_recording()
# ... kayıt devam ediyor ...
audio_file = recorder.stop_recording()  # -> "temp/recording_1736659200000.wav"
```

---

## `transcriber.py` - Groq API Transkripsiyon

**Amaç:** Ses dosyasını metne çevirme (Speech-to-Text)

**Sınıf:** `GroqTranscriber`

**Önemli Metotlar:**
- `transcribe(audio_file_path, language="tr")` - Transkripsiyon yapar
- `transcribe_with_language(audio_file_path, language)` - Açık dil belirterek transkribe et
- `test_api_key()` - API key'in geçerli olup olmadığını kontrol eder

**Teknik Detaylar:**
- **API:** Groq Cloud (whisper-large-v3 modeli)
- **Kimlik Doğrulama:** `GROQ_API_KEY` .env dosyasından
- **Dil Desteği:** Türkçe (`language="tr"`) - yüksek doğruluk
- **Retry Logic:** Ağ hataları için 3 deneme, exponential backoff
- **Hata Yönetimi:** 401 (invalid key), network errors

**Hata Kodları:**
- `ValueError`: API key bulunamadı
- `None`: Transkripsiyon başarısız (network/API hatası)

**Kullanım Örneği:**
```python
transcriber = GroqTranscriber()
text = transcriber.transcribe("temp/recording.wav", language="tr")
# -> "merhaba nasılsın"
```

---

## `input_simulator.py` - Metin Enjektörü

**Amaç:** Transkribe edilmiş metni aktif pencere yapıştırmak

**Sınıf:** `TextInjector`

**Önemli Metotlar:**
- `inject_text(text)` - Metni clipboard kullanarak yapıştırır
- `inject_text_direct(text, char_delay)` - Klavye simülasyonu (fallback)

**Teknik Detaylar:**
- **Kütüphane:** `pyperclip` (clipboard) + `pyautogui` (hotkeys)
- **Unicode Desteği:** Türkçe karakterler (ş, ı, ğ, ö, ç, ü) ✅
- **Yöntem:** Clipboard backup → Copy → Ctrl+V → Restore
- **Gecikme:** Yapıştırmadan sonra 100ms bekleme

**Clipboard Koruma:**
Kullanıcının mevcut clipboard içeriği korunur, yapıştırmadan sonra geri yüklenir.

**Kullanım Örneği:**
```python
injector = TextInjector()
injector.inject_text("merhaba dünya")  # Aktif pencere yapıştırır
```

---

## `history_manager.py` - Kayıt Geçmişi Yöneticisi

**Amaç:** Oturum sırasında yapılan kayıtları bellekte tutma

**Sınıf:** `HistoryManager`

**Önemli Metotlar:**
- `add_recording(filepath)` - Kaydı geçmişe ekler, ID döndürür
- `get_recordings()` - Tüm kayıtları listeler (yeni → eski)
- `update_transcript(id, text)` - Transkripsiyon sonucunu kaydeder
- `delete_recording(id)` - Kaydı geçmişten siler
- `clear_all()` - Tüm geçmişi temizler
- `get_selected_recordings(selected_state)` - Seçili kayıtları döndürür

**Veri Modeli (`Recording`):**
```python
@dataclass
class Recording:
    id: str              # Timestamp (benzersiz)
    filepath: str        # .wav dosya yolu
    created_at: datetime # Oluşturulma zamanı
    transcribed: bool    # Transkribe edildi mi?
    transcript: str      # Transkribe metin
```

**Yaşam Döngüsü:**
1. Kayıt durdurulur → `add_recording()` çağrılır
2. Kayıt UI'de görünür
3. Kullanıcı checkbox ile seçer
4. "Transcribe Selected" ile transkribe edilir
5. Uygulama kapanınca → tüm kayıtlar silinir (temp dosyalarıyla birlikte)

---

## Dosya Yapısı

```
src/core/
├── recorder.py          # Ses kaydedici (sounddevice + numpy)
├── transcriber.py       # Groq API transkripsiyon
├── input_simulator.py   # Metin enjektörü (clipboard + pyautogui)
└── history_manager.py   # Kayıt geçmişi yöneticisi
```

---

## Bağımlılıklar

```
core/
├── recorder.py → sounddevice, numpy
├── transcriber.py → groq, config
├── input_simulator.py → pyperclip, pyautogui
└── history_manager.py → models.recording, datetime, pathlib
```
