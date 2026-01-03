# 🔍 Bir Bilene Danış - Mentorluk Platformu (Full Stack)

Bu depo, ders ödevi için geliştirilmiş **full stack** bir mentorluk platformudur. Python Flask backend ve modern HTML/CSS/JavaScript frontend içerir.

## 📋 Özellikler

- ✅ **JWT Token Tabanlı Kimlik Doğrulama** - Güvenli kullanıcı girişi ve yetkilendirme
- ✅ **Uzmanlık Alanı Bazlı Mentor Arama** - 8 farklı uzmanlık alanı ve her alan için uzmanlar
- ✅ **Danışma Sistemi** - Mentora mesaj gönderme ve danışma geçmişi takibi
- ✅ **Kullanıcı Profili** - Kişisel profil ve danışma geçmişi görüntüleme
- ✅ **Platform İstatistikleri** - Genel platform verileri
- ✅ **Docker Compose Desteği** - 2 port üzerinden servis (Backend: 5000, Frontend: 8080)
- ✅ **CORS Desteği** - Frontend-Backend iletişimi için

## 🏗️ Mimari

- **Backend**: Python Flask REST API (Port 5000)
- **Frontend**: HTML/CSS/JavaScript (Nginx, Port 8080)
- **Veritabanı**: PostgreSQL veya MongoDB (Docker ile)
- **Kimlik Doğrulama**: JWT (JSON Web Token)

## 🚀 Hızlı Başlangıç

### Yöntem 1: Docker Compose ile Çalıştırma (Önerilen)

#### Gereksinimler:
- Docker Desktop kurulu ve çalışıyor olmalı
- [Docker Desktop İndir](https://www.docker.com/products/docker-desktop/)

#### PostgreSQL ile Çalıştırma (Varsayılan):

1. **Proje klasörüne gidin:**
```bash
cd BirBileneDanis-main
```

2. **Docker Compose ile servisleri başlatın:**
```bash
docker compose up -d --build
```

Bu komut şunları başlatır:
- PostgreSQL veritabanı (port 5432)
- Backend uygulaması (port 5000)
- Frontend uygulaması (port 8080)

3. **Servislerin çalıştığını kontrol edin:**
```bash
docker compose ps
```

4. **Uygulamalara erişin:**
- **Backend API:** http://localhost:5000
- **Frontend:** http://localhost:8080

5. **Servisleri durdurmak için:**
```bash
docker compose down
```

#### MongoDB ile Çalıştırma:

1. **MongoDB versiyonunu başlatın:**
```bash
docker compose -f docker-compose.mongodb.yml up -d --build
```

Bu komut şunları başlatır:
- MongoDB veritabanı (port 27017)
- Backend uygulaması (MongoDB versiyonu, port 5000)
- Frontend uygulaması (port 8080)

2. **Servisleri durdurmak için:**
```bash
docker compose -f docker-compose.mongodb.yml down
```

**Not:** Detaylı veritabanı kurulum bilgileri için `VERITABANI_KURULUM.md` dosyasına bakın.

### Yöntem 2: Manuel Çalıştırma (Docker olmadan)

#### Gereksinimler:
- Python 3.11 veya üzeri
- pip (Python paket yöneticisi)

#### Backend'i Çalıştırma:

1. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

2. **Backend'i başlatın:**
```bash
python app.py
```

Backend şu adreste çalışacak: **http://localhost:5000**

#### Frontend'i Çalıştırma:

**Seçenek A: Python'un basit HTTP sunucusunu kullanın**

Yeni bir terminal penceresi açın:
```bash
cd frontend
python -m http.server 8080
```

Ardından tarayıcıda **http://localhost:8080** adresine gidin.

**Seçenek B: Frontend dosyasını doğrudan tarayıcıda açın**

`frontend/index.html` dosyasına çift tıklayarak tarayıcıda açabilirsiniz.

## 🔐 Kullanıcı Hesapları

Sistemde önceden tanımlı kullanıcılar:

| E-posta | Şifre | Rol |
|---------|-------|-----|
| `kullanici@mail.com` | `123456` | kullanici |
| `mentor@mail.com` | `123456` | mentor |

## 📚 API Endpoint'leri

### 🔓 Açık Endpoint'ler (Token Gerektirmez)

#### Sağlık Kontrolü
```http
GET /
```
**Yanıt:**
```json
{
  "message": "Bir Bilene Danış API'si hazır!"
}
```

#### Kullanıcı Girişi
```http
POST /kullanici/giris
Content-Type: application/json

{
  "eposta": "kullanici@mail.com",
  "sifre": "123456"
}
```
**Yanıt:**
```json
{
  "durum": "basarili",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Uzmanlık Alanlarını Listele
```http
GET /uzmanlik/alanlar
```
**Yanıt:**
```json
{
  "alanlar": [
    "Dijital Pazarlama",
    "Finans ve Yatırım",
    "İşletme ve Girişimcilik",
    "Kariyer Planlama",
    "Veri Bilimi",
    "Web Tasarım",
    "Yazılım Geliştirme"
  ]
}
```

#### Mentor Arama
```http
GET /mentor/ara?alan=Yazılım Geliştirme&dil=tr
```
**Yanıt:**
```json
[
  {
    "mentorId": 45,
    "adSoyad": "Ayşe Demir",
    "uzmanlikAlani": "Yazılım Geliştirme",
    "derecelendirme": 4.8,
    "deneyimYili": 10,
    "bioKisa": "10 yıllık deneyimli tam yığın geliştirici.",
    "dil": "tr"
  }
]
```

#### Tüm Mentorları Listele
```http
GET /mentor/liste
```

#### Platform İstatistikleri
```http
GET /istatistikler
```

#### Public API Endpoint'leri (Yeni)

##### Rastgele Şaka
```http
GET /api/public/joke
```
**Yanıt:**
```json
{
  "durum": "basarili",
  "setup": "Şaka sorusu...",
  "punchline": "Şaka cevabı...",
  "kaynak": "official-joke-api.appspot.com"
}
```

##### Rastgele Alıntı
```http
GET /api/public/quote
```
**Yanıt:**
```json
{
  "durum": "basarili",
  "content": "Alıntı metni...",
  "author": "Yazar adı",
  "tags": ["tag1", "tag2"],
  "kaynak": "api.quotable.io"
}
```

##### Kedi Bilgisi
```http
GET /api/public/cat-fact
```

##### Hava Durumu
```http
GET /api/public/weather?city=Istanbul
```

##### Ülke Listesi
```http
GET /api/public/countries
```

### 🔒 Korumalı Endpoint'ler (JWT Token Gerekli)

Tüm korumalı endpoint'ler için `Authorization` header'ında Bearer token göndermeniz gerekir:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Danışma Gönder
```http
POST /danisma/gonder
Authorization: Bearer <token>
Content-Type: application/json

{
  "mentorId": 45,
  "soruBasligi": "Microservice Mimarisi Hakkında",
  "soruIcerigi": "Büyük bir projede monolith yapıdan microservice'e geçiş için önerileriniz nelerdir?"
}
```

#### Kullanıcı Profili
```http
GET /kullanici/profil
Authorization: Bearer <token>
```

#### Danışma Geçmişi
```http
GET /danisma/gecmis
Authorization: Bearer <token>
```

#### Danışma Durumu
```http
GET /danisma/<danisma_id>
Authorization: Bearer <token>
```

#### Mentor Oyla
```http
POST /mentor/<mentor_id>/oyla
Authorization: Bearer <token>
Content-Type: application/json

{
  "oy": 5
}
```

#### Kullanıcı Kayıt
```http
POST /kullanici/kayit
Content-Type: application/json

{
  "eposta": "yeni@mail.com",
  "sifre": "123456",
  "adSoyad": "Yeni Kullanıcı"
}
```

## 🎯 Uzmanlık Alanları

Sistemde şu uzmanlık alanları mevcuttur (her alan için en az 1 uzman):

1. **Yazılım Geliştirme** - 2 uzman
2. **Kariyer Planlama** - 2 uzman
3. **Veri Bilimi** - 1 uzman
4. **Web Tasarım** - 1 uzman
5. **İşletme ve Girişimcilik** - 1 uzman
6. **Dijital Pazarlama** - 1 uzman
7. **Finans ve Yatırım** - 1 uzman

## 💻 Frontend Kullanımı

1. **Giriş Yapın:**
   - Frontend'e gidin: http://localhost:8080
   - E-posta: `kullanici@mail.com`
   - Şifre: `123456`
   - "Giriş Yap" butonuna tıklayın

2. **Mentor Ara:**
   - "Uzmanlık Alanı Seçin" dropdown'ından bir alan seçin
   - İsteğe bağlı olarak dil filtresi uygulayın
   - "Mentorları Listele" butonuna tıklayın

3. **Mentora Mesaj Gönder:**
   - Listelenen mentorların yanındaki "💬 Mesaj Gönder" butonuna tıklayın
   - Soru başlığı ve içeriğini girin
   - "Mesaj başarıyla gönderildi" mesajını göreceksiniz

4. **Profil ve Geçmiş:**
   - "Kullanıcı Profilim" bölümünden profil bilgilerinizi görüntüleyin
   - "Danışma Geçmişim" bölümünden tüm danışmalarınızı görüntüleyin

## 🐳 Docker Compose Yapılandırması

Proje 2 servis içerir:

1. **bir_bilene_danis_backend** (Port 5000)
   - Flask uygulaması
   - Python 3.11-slim base image
   - Otomatik restart

2. **bir_bilene_danis_frontend** (Port 8080)
   - Nginx static file server
   - Frontend klasörünü serve eder
   - Backend'e bağımlı (depends_on)

## 🔧 Geliştirme

### Backend Geliştirme

```bash
# Sanal ortam oluştur (opsiyonel)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Backend'i çalıştır
python app.py
```

### Frontend Geliştirme

Frontend klasöründeki `index.html` dosyasını düzenleyebilirsiniz. Değişiklikler anında yansır (Docker kullanıyorsanız sayfayı yenileyin).

## 📦 Bağımlılıklar

### Backend
- `flask==3.0.3` - Web framework
- `pyjwt==2.9.0` - JWT token işlemleri
- `flask-cors==4.0.0` - CORS desteği
- `psycopg2-binary==2.9.9` - PostgreSQL driver
- `pymongo==4.6.1` - MongoDB driver
- `python-dotenv==1.0.0` - Environment variable yönetimi
- `requests==2.31.0` - HTTP istekleri için (Public API entegrasyonu)

### MCP Server
- `mcp>=0.9.0` - Model Context Protocol SDK
- `requests>=2.31.0` - HTTP istekleri için

## 🧪 Test Etme

### cURL ile Test

```bash
# Sağlık kontrolü
curl http://localhost:5000/

# Giriş yap
curl -X POST http://localhost:5000/kullanici/giris \
  -H "Content-Type: application/json" \
  -d '{"eposta":"kullanici@mail.com","sifre":"123456"}'

# Token ile danışma gönder (TOKEN'i yukarıdaki komuttan al)
curl -X POST http://localhost:5000/danisma/gonder \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"mentorId":45,"soruBasligi":"Test","soruIcerigi":"Test mesajı"}'
```

## 📝 Proje Yapısı

```
BirBileneDanis-main/
├── app.py                      # Flask backend uygulaması (PostgreSQL)
├── app_mongodb.py              # Flask backend uygulaması (MongoDB)
├── requirements.txt            # Python bağımlılıkları
├── Dockerfile                  # Backend Docker imajı
├── docker-compose.yml          # Docker Compose yapılandırması (PostgreSQL)
├── docker-compose.mongodb.yml  # Docker Compose yapılandırması (MongoDB)
├── init_db.sql                 # PostgreSQL başlangıç şeması
├── init_mongodb.js             # MongoDB başlangıç verileri
├── swagger.yaml                # API dokümantasyonu
├── VERITABANI_KURULUM.md       # Veritabanı kurulum rehberi
├── frontend/
│   └── index.html              # Frontend uygulaması
├── mcp-server/                 # MCP (Model Context Protocol) Server
│   ├── server.py               # MCP server ana dosyası
│   ├── test_server.py          # MCP server test scripti
│   ├── requirements.txt        # MCP server bağımlılıkları
│   └── README.md               # MCP server dokümantasyonu
└── README.md                   # Bu dosya
```

## 🤖 MCP Server

Proje, Model Context Protocol (MCP) uyumlu bir server içerir. MCP server, AI modellerinin kullanabileceği tool fonksiyonları sağlar.

### MCP Server Özellikleri

- ✅ **7 Tool Fonksiyonu** - Matematiksel işlemler ve public API entegrasyonları
- ✅ **Public API Desteği** - Şakalar, alıntılar, kedi bilgileri, hava durumu
- ✅ **İstatistik Hesaplama** - Sayı listelerinin istatistiklerini hesaplama

### MCP Server Kullanımı

Detaylı bilgi için `mcp-server/README.md` dosyasına bakın.

**Hızlı Başlangıç:**
```bash
cd mcp-server
pip install -r requirements.txt
python server.py
```

## 🔒 Güvenlik Notları

- JWT token'lar 1 saat geçerlidir
- Token'lar localStorage'da saklanır (production'da daha güvenli bir yöntem kullanılmalıdır)
- CORS tüm origin'lere açıktır (production'da sınırlandırılmalıdır)
- Şifreler plain text olarak saklanır (production'da hash'lenmelidir)
- Public API'ler rate limiting olabilir

## 🐛 Sorun Giderme

### Docker Compose hatası alıyorsanız:
- Docker Desktop'ın çalıştığından emin olun
- Portların (5000 ve 8080) başka bir uygulama tarafından kullanılmadığından emin olun
- `docker compose config` komutu ile syntax kontrolü yapın

### Backend çalışmıyorsa:
- Python versiyonunu kontrol edin: `python --version`
- Paketlerin yüklü olduğundan emin olun: `pip list`
- Port 5000'in kullanılabilir olduğundan emin olun

### Frontend backend'e bağlanamıyorsa:
- Backend'in çalıştığından emin olun
- Tarayıcı konsolunda (F12) hata mesajlarını kontrol edin
- CORS hatası alıyorsanız, backend'in CORS desteğinin aktif olduğundan emin olun

## 📄 Lisans

Bu proje ders ödevi amaçlı geliştirilmiştir.

## 👥 Katkıda Bulunanlar

- Proje ödevi çıktısı

---

**Proje Ödevi Çıktısı | Python Flask Backend & Frontend & Docker**
