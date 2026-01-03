-- Bir Bilene Danış Veritabanı Şema Oluşturma Scripti

-- Kullanıcılar Tablosu
CREATE TABLE IF NOT EXISTS kullanicilar (
    kullanici_id SERIAL PRIMARY KEY,
    eposta VARCHAR(255) UNIQUE NOT NULL,
    sifre VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL DEFAULT 'kullanici',
    ad_soyad VARCHAR(255),
    kayit_tarihi DATE DEFAULT CURRENT_DATE,
    olusturma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mentorlar Tablosu
CREATE TABLE IF NOT EXISTS mentorlar (
    mentor_id SERIAL PRIMARY KEY,
    ad_soyad VARCHAR(255) NOT NULL,
    uzmanlik_alani VARCHAR(255) NOT NULL,
    derecelendirme DECIMAL(3,2) DEFAULT 0.0,
    deneyim_yili INTEGER DEFAULT 0,
    bio_kisa TEXT,
    dil VARCHAR(10) DEFAULT 'tr',
    olusturma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mentor Oyları Tablosu
CREATE TABLE IF NOT EXISTS mentor_oylari (
    oy_id SERIAL PRIMARY KEY,
    mentor_id INTEGER NOT NULL REFERENCES mentorlar(mentor_id) ON DELETE CASCADE,
    kullanici_id INTEGER NOT NULL REFERENCES kullanicilar(kullanici_id) ON DELETE CASCADE,
    oy INTEGER NOT NULL CHECK (oy >= 1 AND oy <= 5),
    olusturma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(mentor_id, kullanici_id)
);

-- Danışmalar Tablosu
CREATE TABLE IF NOT EXISTS danismalar (
    danisma_id VARCHAR(50) PRIMARY KEY,
    kullanici_id INTEGER NOT NULL REFERENCES kullanicilar(kullanici_id) ON DELETE CASCADE,
    mentor_id INTEGER NOT NULL REFERENCES mentorlar(mentor_id) ON DELETE CASCADE,
    soru_basligi VARCHAR(500),
    soru_icerigi TEXT NOT NULL,
    durum VARCHAR(50) DEFAULT 'beklemede',
    yanit TEXT,
    olusturma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- İndeksler
CREATE INDEX IF NOT EXISTS idx_danismalar_kullanici ON danismalar(kullanici_id);
CREATE INDEX IF NOT EXISTS idx_danismalar_mentor ON danismalar(mentor_id);
CREATE INDEX IF NOT EXISTS idx_danismalar_durum ON danismalar(durum);
CREATE INDEX IF NOT EXISTS idx_mentorlar_uzmanlik ON mentorlar(uzmanlik_alani);
CREATE INDEX IF NOT EXISTS idx_mentor_oylari_mentor ON mentor_oylari(mentor_id);

-- Başlangıç Verileri: Kullanıcılar
INSERT INTO kullanicilar (eposta, sifre, rol, ad_soyad, kayit_tarihi) VALUES
    ('mentor@mail.com', '123456', 'mentor', 'Ayşe Demir', '2024-01-15'),
    ('kullanici@mail.com', '123456', 'kullanici', 'Ahmet Yılmaz', '2024-02-20')
ON CONFLICT (eposta) DO NOTHING;

-- Başlangıç Verileri: Mentorlar
INSERT INTO mentorlar (mentor_id, ad_soyad, uzmanlik_alani, derecelendirme, deneyim_yili, bio_kisa, dil) VALUES
    (45, 'Ayşe Demir', 'Yazılım Geliştirme', 4.8, 10, '10 yıllık deneyimli tam yığın geliştirici. Python, JavaScript ve Java konusunda uzman.', 'tr'),
    (47, 'Cem Yılmaz', 'Yazılım Geliştirme', 4.9, 8, 'Bulut mimarileri ve mikroservisler üzerine çalışan mentor.', 'en'),
    (46, 'Burak Kaya', 'Kariyer Planlama', 4.5, 7, 'Kariyer planlama ve mülakat koçluğu konusunda uzman.', 'tr'),
    (48, 'Zeynep Öztürk', 'Kariyer Planlama', 4.7, 9, 'HR uzmanı ve kariyer danışmanı. CV hazırlama ve iş görüşmesi teknikleri konusunda deneyimli.', 'tr'),
    (49, 'Mehmet Şahin', 'Veri Bilimi', 4.6, 6, 'Machine Learning ve veri analizi konusunda uzman. Python, R ve SQL kullanıyor.', 'tr'),
    (50, 'Elif Yıldız', 'Web Tasarım', 4.8, 5, 'UI/UX tasarımcı ve frontend geliştirici. React, Vue.js ve modern web teknolojileri konusunda uzman.', 'tr'),
    (51, 'Can Arslan', 'İşletme ve Girişimcilik', 4.5, 12, 'İş geliştirme ve girişimcilik konusunda deneyimli mentor. Startup kurma ve yönetimi.', 'tr'),
    (52, 'Selin Aydın', 'Dijital Pazarlama', 4.7, 8, 'SEO, SEM ve sosyal medya pazarlama konusunda uzman. Marka yönetimi ve içerik stratejisi.', 'tr'),
    (53, 'Emre Doğan', 'Finans ve Yatırım', 4.6, 11, 'Finansal planlama, yatırım stratejileri ve kişisel finans yönetimi konusunda uzman.', 'tr')
ON CONFLICT DO NOTHING;

-- Başlangıç Verileri: Mentor Oyları
INSERT INTO mentor_oylari (mentor_id, kullanici_id, oy) VALUES
    (45, 102, 5), (45, 102, 5), (45, 102, 4), (45, 102, 5), (45, 102, 4),
    (46, 102, 4), (46, 102, 5), (46, 102, 4), (46, 102, 5), (46, 102, 4),
    (47, 102, 5), (47, 102, 5), (47, 102, 5), (47, 102, 5), (47, 102, 4),
    (48, 102, 5), (48, 102, 4), (48, 102, 5), (48, 102, 4), (48, 102, 5),
    (49, 102, 4), (49, 102, 5), (49, 102, 5), (49, 102, 4), (49, 102, 5),
    (50, 102, 5), (50, 102, 5), (50, 102, 4), (50, 102, 5), (50, 102, 4),
    (51, 102, 4), (51, 102, 5), (51, 102, 5), (51, 102, 5), (51, 102, 4),
    (52, 102, 5), (52, 102, 4), (52, 102, 5), (52, 102, 5), (52, 102, 4),
    (53, 102, 4), (53, 102, 5), (53, 102, 4), (53, 102, 5), (53, 102, 5)
ON CONFLICT DO NOTHING;

