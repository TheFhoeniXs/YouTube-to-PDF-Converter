# Transcriptor App

YouTube videolarından transcript alıp PDF'e dönüştüren masaüstü uygulaması.

## Özellikler

- ✅ YouTube video transcript'lerini otomatik çekme
- 📄 Transcript'leri PDF formatına dönüştürme
- 🎨 Modern ve kullanıcı dostu arayüz
- ⚡ Asenkron işlem kuyruğu
- 💾 Ayarları kalıcı olarak kaydetme

## Gereksinimler

- Python 3.9 veya üzeri
- UV veya Poetry paket yöneticisi

## Kurulum

### UV ile

Projeyi klonlayın ve bağımlılıkları yükleyin:
```bash
git clone <repository-url>
cd transcriptor
uv sync
```

### Poetry ile
```bash
git clone <repository-url>
cd transcriptor
poetry install
```

## Uygulamayı Çalıştırma

### UV

Masaüstü uygulaması olarak çalıştır:
```bash
uv run flet run
```

Web uygulaması olarak çalıştır:
```bash
uv run flet run --web
```

### Poetry

Masaüstü uygulaması olarak çalıştır:
```bash
poetry run flet run
```

Web uygulaması olarak çalıştır:
```bash
poetry run flet run --web
```

## Kullanım

1. **Ayarlar**: Sağ üst köşedeki ayarlar butonuna tıklayın
2. **API Key**: YouTube Transcript API anahtarınızı girin
3. **Klasör Seç**: PDF'lerin kaydedileceği klasörü seçin
4. **Kaydet**: Ayarları kaydedin
5. **URL Gir**: YouTube video URL'sini girin
6. **Convert**: "Convert to PDF" butonuna tıklayın

## Uygulama Paketleme

### Android

APK dosyası oluştur:
```bash
flet build apk -v
```

AAB (Android App Bundle) oluştur:
```bash
flet build aab -v
```

Detaylı bilgi için: [Android Packaging Guide](https://flet.dev/docs/publish/android/)

### iOS

IPA dosyası oluştur:
```bash
flet build ipa -v
```

**Not**: iOS build için macOS gereklidir.

Detaylı bilgi için: [iOS Packaging Guide](https://flet.dev/docs/publish/ios/)

### macOS

macOS uygulaması oluştur:
```bash
flet build macos -v
```

**Not**: macOS build için macOS gereklidir.

Detaylı bilgi için: [macOS Packaging Guide](https://flet.dev/docs/publish/macos/)

### Linux

Linux paketi oluştur:
```bash
flet build linux -v
```

Detaylı bilgi için: [Linux Packaging Guide](https://flet.dev/docs/publish/linux/)

### Windows

Windows kurulum dosyası oluştur:
```bash
flet build windows -v
```

Detaylı bilgi için: [Windows Packaging Guide](https://flet.dev/docs/publish/windows/)

## Proje Yapısı
```
transcriptor/
├── src/
│   ├── main.py                 # Ana uygulama dosyası
│   ├── services/
│   │   ├── transcript.py       # YouTube transcript servisi
│   │   ├── pdf_generate.py     # PDF oluşturma servisi
│   │   └── settings_manager.py # Ayarlar yönetimi
│   └── assets/                 # Görsel ve kaynak dosyaları
├── pyproject.toml              # Proje bağımlılıkları
├── settings.json               # Kullanıcı ayarları (otomatik oluşur)
└── README.md                   # Bu dosya
```

## Bağımlılıklar

- **flet**: Modern UI framework
- **reportlab**: PDF oluşturma kütüphanesi
- **aiohttp**: Asenkron HTTP istekleri

## Sorun Giderme

### API Key hatası
- Geçerli bir YouTube Transcript API anahtarı girdiğinizden emin olun
- Ayarlar menüsünden API anahtarınızı kontrol edin

### Klasör seçimi sorunu
- Yazma izniniz olan bir klasör seçtiğinizden emin olun
- Windows'ta C:\Users\KullanıcıAdı\Documents klasörünü deneyin

### PDF oluşturma hatası
- İndirme klasörünün var olduğundan emin olun
- Disk alanınızın yeterli olduğunu kontrol edin

## Lisans

[Lisans bilgisi buraya eklenecek]

## Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için lütfen önce bir issue açarak ne değiştirmek istediğinizi tartışın.

## İletişim

- Geliştirici: [İsminiz]
- Email: you@example.com
- GitHub: [GitHub profiliniz]

## Teşekkürler

Bu proje [Flet](https://flet.dev/) framework'ü kullanılarak geliştirilmiştir.

---

Daha fazla bilgi için [Flet Documentation](https://flet.dev/docs/) sayfasını ziyaret edin.