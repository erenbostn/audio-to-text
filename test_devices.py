"""Son kaydedilen ses dosyasını analiz et"""
import wave
import numpy as np
from pathlib import Path

temp_dir = Path("temp")
wav_files = list(temp_dir.glob("recording_*.wav"))

with open("audio_analysis.txt", "w", encoding="utf-8") as f:
    if not wav_files:
        f.write("Kayit dosyasi bulunamadi!\n")
    else:
        latest = max(wav_files, key=lambda x: x.stat().st_mtime)
        f.write(f"Dosya: {latest.name}\n")
        f.write("=" * 50 + "\n")
        
        with wave.open(str(latest), 'rb') as wav:
            frames = wav.getnframes()
            rate = wav.getframerate()
            duration = frames / rate
            
            f.write(f"Sure: {duration:.2f} saniye\n")
            f.write(f"Sample Rate: {rate} Hz\n")
            f.write(f"Frame: {frames}\n")
            
            raw_data = wav.readframes(frames)
            audio = np.frombuffer(raw_data, dtype=np.int16)
            
            max_amp = np.max(np.abs(audio))
            mean_amp = np.mean(np.abs(audio))
            
            f.write(f"\nSes Analizi:\n")
            f.write(f"  Max Amplitude: {max_amp} (max olasi: 32767)\n")
            f.write(f"  Ortalama: {mean_amp:.2f}\n")
            f.write(f"  Yuzde: {(max_amp/32767)*100:.1f}%\n")
            
            if max_amp < 100:
                f.write("\nSONUC: SES YOK veya COK DUSUK!\n")
                f.write("Mikrofon izinlerini kontrol edin.\n")
            elif max_amp < 1000:
                f.write("\nSONUC: Ses seviyesi dusuk.\n")
            else:
                f.write("\nSONUC: Ses seviyesi normal.\n")

print("Sonuc audio_analysis.txt dosyasina yazildi!")
