# MermaidJS Diyagramları

Bu dosya, "Bir Bilene Danış" uygulamasının çeşitli süreçlerini görselleştiren MermaidJS diyagramlarını içerir.

## 1. Kullanıcı Kimlik Doğrulama Akışı (JWT Token)

```mermaid
sequenceDiagram
    participant User as Kullanıcı
    participant Frontend as Frontend
    participant Backend as Backend API
    participant DB as Veritabanı
    
    User->>Frontend: E-posta ve Şifre Girer
    Frontend->>Backend: POST /kullanici/giris
    Backend->>DB: Kullanıcı Bilgilerini Sorgula
    DB-->>Backend: Kullanıcı Verileri
    
    alt Kimlik Doğrulama Başarılı
        Backend->>Backend: JWT Token Oluştur
        Backend-->>Frontend: Token Döndür (200 OK)
        Frontend->>Frontend: Token'ı localStorage'a Kaydet
        Frontend-->>User: Giriş Başarılı
    else Kimlik Doğrulama Başarısız
        Backend-->>Frontend: Hata Mesajı (401 Unauthorized)
        Frontend-->>User: Geçersiz Bilgiler
    end
```

## 2. Danışma Gönderme Akışı (JWT Korumalı Endpoint)

```mermaid
sequenceDiagram
    participant User as Kullanıcı
    participant Frontend as Frontend
    participant Backend as Backend API
    participant DB as Veritabanı
    
    User->>Frontend: Mentor Seçer ve Soru Yazar
    Frontend->>Backend: POST /danisma/gonder<br/>(Authorization: Bearer Token)
    
    Backend->>Backend: JWT Token Doğrula
    
    alt Token Geçerli
        Backend->>DB: Mentor Varlığını Kontrol Et
        DB-->>Backend: Mentor Bulundu
        Backend->>DB: Danışma Kaydı Oluştur
        DB-->>Backend: Danışma ID
        Backend-->>Frontend: Başarılı (201 Created)
        Frontend-->>User: Mesaj Gönderildi
    else Token Geçersiz
        Backend-->>Frontend: 403 Forbidden
        Frontend-->>User: Yetkilendirme Hatası
    else Mentor Bulunamadı
        Backend-->>Frontend: 404 Not Found
        Frontend-->>User: Mentor Bulunamadı
    end
```

## 3. Sistem Mimarisi

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Tarayıcı]
    end
    
    subgraph "Docker Compose Environment"
        Frontend[Frontend<br/>Nginx:8080]
        Backend[Backend API<br/>Flask:5000]
        
        subgraph "Database Options"
            PostgreSQL[(PostgreSQL<br/>Port:5432)]
            MongoDB[(MongoDB<br/>Port:27017)]
        end
    end
    
    Browser -->|HTTP/8080| Frontend
    Browser -->|HTTP/5000| Backend
    Frontend -.->|Proxy| Backend
    Backend -->|SQL| PostgreSQL
    Backend -->|NoSQL| MongoDB
    
    style Frontend fill:#61dafb
    style Backend fill:#3776ab
    style PostgreSQL fill:#336791
    style MongoDB fill:#47a248
```

## 4. API Endpoint'leri Akış Diyagramı

```mermaid
graph LR
    subgraph "Public Endpoints (JWT Gerekmez)"
        Health[GET /<br/>Sağlık Kontrolü]
        Login[POST /kullanici/giris<br/>Giriş Yap]
        Register[POST /kullanici/kayit<br/>Kayıt Ol]
        SearchMentor[GET /mentor/ara<br/>Mentor Ara]
        ListMentor[GET /mentor/liste<br/>Tüm Mentorlar]
        Expertise[GET /uzmanlik/alanlar<br/>Uzmanlık Alanları]
        Stats[GET /istatistikler<br/>Platform İstatistikleri]
        Joke[GET /api/public/joke<br/>Rastgele Şaka]
        Quote[GET /api/public/quote<br/>Rastgele Alıntı]
        Swagger[GET /api/docs<br/>Swagger UI]
    end
    
    subgraph "Protected Endpoints (JWT Gerekli)"
        SendConsult[POST /danisma/gonder<br/>Danışma Gönder]
        Profile[GET /kullanici/profil<br/>Profil Bilgileri]
        History[GET /danisma/gecmis<br/>Danışma Geçmişi]
        ConsultStatus[GET /danisma/:id<br/>Danışma Durumu]
        VoteMentor[POST /mentor/:id/oyla<br/>Mentor Oyla]
    end
    
    User[Kullanıcı] -->|Token Yok| Public
    User -->|Token Var| Protected
    
    Public --> Health & Login & Register & SearchMentor & ListMentor & Expertise & Stats & Joke & Quote & Swagger
    Protected --> SendConsult & Profile & History & ConsultStatus & VoteMentor
    
    style Public fill:#90EE90
    style Protected fill:#FFB6C1
```

## 5. Veritabanı İlişkileri (PostgreSQL)

```mermaid
erDiagram
    kullanicilar ||--o{ danismalar : "gönderir"
    mentorlar ||--o{ danismalar : "alır"
    mentorlar ||--o{ mentor_oylari : "sahip olur"
    kullanicilar ||--o{ mentor_oylari : "oluşturur"
    
    kullanicilar {
        int kullanici_id PK
        varchar eposta UK
        varchar sifre
        varchar rol
        varchar ad_soyad
        timestamp kayit_tarihi
    }
    
    mentorlar {
        int mentor_id PK
        varchar ad_soyad
        varchar uzmanlik_alani
        decimal derecelendirme
        int deneyim_yili
        text bio_kisa
        varchar dil
    }
    
    danismalar {
        varchar danisma_id PK
        int kullanici_id FK
        int mentor_id FK
        varchar soru_basligi
        text soru_icerigi
        varchar durum
        timestamp olusturma_tarihi
    }
    
    mentor_oylari {
        int oy_id PK
        int mentor_id FK
        int kullanici_id FK
        int oy
        timestamp oy_tarihi
    }
```

## 6. Docker Compose Servis İlişkileri

```mermaid
graph TB
    subgraph "PostgreSQL Stack"
        PG_DB[PostgreSQL Database<br/>Port: 5432]
        PG_Backend[Backend<br/>app.py<br/>Port: 5000]
        PG_Frontend[Frontend<br/>Nginx<br/>Port: 8080]
    end
    
    subgraph "MongoDB Stack"
        Mongo_DB[MongoDB Database<br/>Port: 27017]
        Mongo_Backend[Backend<br/>app_mongodb.py<br/>Port: 5000]
        Mongo_Frontend[Frontend<br/>Nginx<br/>Port: 8080]
    end
    
    PG_Backend -->|depends_on| PG_DB
    PG_Frontend -->|depends_on| PG_Backend
    
    Mongo_Backend -->|depends_on| Mongo_DB
    Mongo_Frontend -->|depends_on| Mongo_Backend
    
    style PG_DB fill:#336791
    style PG_Backend fill:#3776ab
    style PG_Frontend fill:#61dafb
    style Mongo_DB fill:#47a248
    style Mongo_Backend fill:#3776ab
    style Mongo_Frontend fill:#61dafb
```

## Diyagramları Görüntüleme

Bu diyagramları görüntülemek için:

1. **GitHub**: Bu dosyayı GitHub'da açın, MermaidJS otomatik olarak render edilir
2. **VS Code**: Mermaid extension yükleyin
3. **Online**: [Mermaid Live Editor](https://mermaid.live/) kullanın
4. **Markdown Preview**: Mermaid destekli bir Markdown görüntüleyici kullanın

## Diyagramların Açıklamaları

### Sequence Diagram 1: Kullanıcı Kimlik Doğrulama
- Kullanıcının sisteme giriş yapma sürecini gösterir
- JWT token oluşturma ve localStorage'a kaydetme adımlarını içerir
- Başarılı ve başarısız senaryoları kapsar

### Sequence Diagram 2: Danışma Gönderme
- JWT token ile korumalı endpoint kullanımını gösterir
- Token doğrulama sürecini detaylandırır
- Mentor kontrolü ve danışma kaydı oluşturma adımlarını içerir

### Architecture Diagram 3: Sistem Mimarisi
- Docker Compose ile çalışan servisleri gösterir
- İki farklı veritabanı seçeneğini (PostgreSQL/MongoDB) gösterir
- Port numaralarını ve bağlantıları gösterir

### Flow Diagram 4: API Endpoints
- Public ve protected endpoint'leri ayırır
- JWT gerektiren ve gerektirmeyen endpoint'leri gruplar
- API'nin tüm yeteneklerini görselleştirir

### ER Diagram 5: Veritabanı Şeması
- PostgreSQL veritabanı tablolarını ve ilişkilerini gösterir
- Primary ve Foreign key ilişkilerini gösterir
- Tablo alanlarını ve veri tiplerini listeler

### Deployment Diagram 6: Docker Compose
- İki farklı deployment seçeneğini gösterir (PostgreSQL ve MongoDB)
- Servisler arası bağımlılıkları gösterir
- Her servisin portlarını belirtir

