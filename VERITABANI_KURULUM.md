# Veritabanı Kurulum Rehberi

Bu proje hem PostgreSQL hem de MongoDB veritabanlarını desteklemektedir.

## PostgreSQL Kurulumu

### 1. Docker Compose ile Çalıştırma

```bash
docker-compose up -d
```

Bu komut şunları başlatır:
- PostgreSQL veritabanı (port 5432)
- Backend uygulaması (port 5000)
- Frontend uygulaması (port 8080)

### 2. Veritabanı Bağlantı Bilgileri

- **Host:** postgres (Docker içinden) veya localhost (dışarıdan)
- **Port:** 5432
- **Database:** birbilenedanis
- **User:** postgres
- **Password:** postgres123

### 3. Veritabanı Şeması

`init_db.sql` dosyası otomatik olarak çalıştırılır ve şu tabloları oluşturur:
- `kullanicilar` - Kullanıcı bilgileri
- `mentorlar` - Mentor bilgileri
- `mentor_oylari` - Mentor oyları
- `danismalar` - Danışma kayıtları

### 4. Manuel Bağlantı (Opsiyonel)

```bash
docker exec -it bir_bilene_danis_postgres psql -U postgres -d birbilenedanis
```

## MongoDB Kurulumu

### 1. Docker Compose ile Çalıştırma

```bash
docker-compose -f docker-compose.mongodb.yml up -d
```

Bu komut şunları başlatır:
- MongoDB veritabanı (port 27017)
- Backend uygulaması (MongoDB versiyonu, port 5000)
- Frontend uygulaması (port 8080)

### 2. Veritabanı Bağlantı Bilgileri

- **Host:** mongodb (Docker içinden) veya localhost (dışarıdan)
- **Port:** 27017
- **Database:** birbilenedanis
- **User:** admin
- **Password:** admin123
- **Connection String:** `mongodb://admin:admin123@mongodb:27017/birbilenedanis?authSource=admin`

### 3. Veritabanı Koleksiyonları

`init_mongodb.js` dosyası otomatik olarak çalıştırılır ve şu koleksiyonları oluşturur:
- `kullanicilar` - Kullanıcı bilgileri
- `mentorlar` - Mentor bilgileri
- `mentor_oylari` - Mentor oyları
- `danismalar` - Danışma kayıtları

### 4. Manuel Bağlantı (Opsiyonel)

```bash
docker exec -it bir_bilene_danis_mongodb mongosh -u admin -p admin123 --authenticationDatabase admin
```

## Uygulama Dosyaları

- **PostgreSQL için:** `app.py` (varsayılan)
- **MongoDB için:** `app_mongodb.py`

## Servisleri Durdurma

```bash
# PostgreSQL versiyonu
docker-compose down

# MongoDB versiyonu
docker-compose -f docker-compose.mongodb.yml down
```

## Verileri Silme

```bash
# PostgreSQL verilerini sil
docker-compose down -v

# MongoDB verilerini sil
docker-compose -f docker-compose.mongodb.yml down -v
```

## Notlar

- İlk çalıştırmada veritabanı şemaları ve başlangıç verileri otomatik olarak oluşturulur
- Veritabanı bağlantı bilgileri environment variable'lar ile yapılandırılabilir
- Her iki veritabanı da aynı API endpoint'lerini kullanır
- Frontend uygulaması her iki versiyonla da çalışır



