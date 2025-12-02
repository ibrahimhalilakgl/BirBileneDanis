# Bir Bilene Danış - Çalıştırma Talimatları

## Yöntem 1: Docker Compose ile Çalıştırma (Önerilen)

### Gereksinimler:
- Docker Desktop kurulu ve çalışıyor olmalı
- [Docker Desktop İndir](https://www.docker.com/products/docker-desktop/)

### Adımlar:

1. **PowerShell'i yönetici olarak açın** ve proje klasörüne gidin:
```powershell
cd "C:\Users\Teatl\OneDrive\Desktop\BirBileneDanis-main"
```

2. **Docker Compose dosyasını kontrol edin:**
```powershell
docker compose config
```
Bu komut syntax hatalarını kontrol eder. Hata yoksa devam edin.

3. **Servisleri başlatın:**
```powershell
docker compose up -d --build
```

4. **Servislerin çalıştığını kontrol edin:**
```powershell
docker compose ps
```

5. **Uygulamalara erişin:**
- **Backend API:** http://localhost:5000
- **Frontend:** http://localhost:8080

6. **Test edin:**
- Tarayıcıda http://localhost:8080 adresine gidin
- "Uzmanlık Alanı" kısmına "Yazılım Geliştirme" yazın
- "Mentorları Listele" butonuna tıklayın

7. **Servisleri durdurmak için:**
```powershell
docker compose down
```

---

## Yöntem 2: Manuel Çalıştırma (Docker olmadan)

### Gereksinimler:
- Python 3.11 veya üzeri
- pip (Python paket yöneticisi)

### Backend'i Çalıştırma:

1. **PowerShell'de proje klasörüne gidin:**
```powershell
cd "C:\Users\Teatl\OneDrive\Desktop\BirBileneDanis-main"
```

2. **Gerekli paketleri yükleyin:**
```powershell
pip install -r requirements.txt
```

3. **Backend'i başlatın:**
```powershell
python app.py
```

Backend şu adreste çalışacak: http://localhost:5000

### Frontend'i Çalıştırma:

Frontend statik bir HTML dosyası olduğu için birkaç seçeneğiniz var:

#### Seçenek A: Python'un basit HTTP sunucusunu kullanın

Yeni bir PowerShell penceresi açın ve şu komutu çalıştırın:
```powershell
cd "C:\Users\Teatl\OneDrive\Desktop\BirBileneDanis-main\frontend"
python -m http.server 8080
```

Ardından tarayıcıda http://localhost:8080 adresine gidin.

#### Seçenek B: Frontend dosyasını doğrudan tarayıcıda açın

`frontend/index.html` dosyasına çift tıklayarak tarayıcıda açabilirsiniz. 
**Not:** Bu yöntemde CORS hatası alabilirsiniz. Backend'i CORS'a izin verecek şekilde yapılandırmanız gerekebilir.

---

## API Endpoint'lerini Test Etme

### 1. Sağlık Kontrolü:
```powershell
curl http://localhost:5000/
```

### 2. Mentor Arama:
```powershell
curl "http://localhost:5000/mentor/ara?alan=Yazılım%20Geliştirme&dil=tr"
```

### 3. Kullanıcı Girişi:
```powershell
curl -X POST http://localhost:5000/kullanici/giris -H "Content-Type: application/json" -d "{\"eposta\":\"kullanici@mail.com\",\"sifre\":\"123456\"}"
```

---

## Sorun Giderme

### Docker Compose hatası alıyorsanız:
- Docker Desktop'ın çalıştığından emin olun
- `docker compose config` komutu ile syntax kontrolü yapın
- Portların (5000 ve 8080) başka bir uygulama tarafından kullanılmadığından emin olun

### Backend çalışmıyorsa:
- Python versiyonunu kontrol edin: `python --version`
- Paketlerin yüklü olduğundan emin olun: `pip list`
- Port 5000'in kullanılabilir olduğundan emin olun

### Frontend backend'e bağlanamıyorsa:
- Backend'in çalıştığından emin olun
- Tarayıcı konsolunda (F12) hata mesajlarını kontrol edin
- CORS hatası alıyorsanız, backend'e CORS desteği eklemeniz gerekebilir


