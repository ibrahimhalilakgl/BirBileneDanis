// MongoDB Başlangıç Verileri

// Veritabanını seç
db = db.getSiblingDB('birbilenedanis');

// Kullanıcılar koleksiyonu
db.kullanicilar.insertMany([
  {
    kullanici_id: 101,
    eposta: 'mentor@mail.com',
    sifre: '123456',
    rol: 'mentor',
    ad_soyad: 'Ayşe Demir',
    kayit_tarihi: '2024-01-15'
  },
  {
    kullanici_id: 102,
    eposta: 'kullanici@mail.com',
    sifre: '123456',
    rol: 'kullanici',
    ad_soyad: 'Ahmet Yılmaz',
    kayit_tarihi: '2024-02-20'
  }
]);

// Mentorlar koleksiyonu
db.mentorlar.insertMany([
  {
    mentor_id: 45,
    ad_soyad: 'Ayşe Demir',
    uzmanlik_alani: 'Yazılım Geliştirme',
    derecelendirme: 4.8,
    deneyim_yili: 10,
    bio_kisa: '10 yıllık deneyimli tam yığın geliştirici. Python, JavaScript ve Java konusunda uzman.',
    dil: 'tr'
  },
  {
    mentor_id: 47,
    ad_soyad: 'Cem Yılmaz',
    uzmanlik_alani: 'Yazılım Geliştirme',
    derecelendirme: 4.9,
    deneyim_yili: 8,
    bio_kisa: 'Bulut mimarileri ve mikroservisler üzerine çalışan mentor.',
    dil: 'en'
  },
  {
    mentor_id: 46,
    ad_soyad: 'Burak Kaya',
    uzmanlik_alani: 'Kariyer Planlama',
    derecelendirme: 4.5,
    deneyim_yili: 7,
    bio_kisa: 'Kariyer planlama ve mülakat koçluğu konusunda uzman.',
    dil: 'tr'
  },
  {
    mentor_id: 48,
    ad_soyad: 'Zeynep Öztürk',
    uzmanlik_alani: 'Kariyer Planlama',
    derecelendirme: 4.7,
    deneyim_yili: 9,
    bio_kisa: 'HR uzmanı ve kariyer danışmanı. CV hazırlama ve iş görüşmesi teknikleri konusunda deneyimli.',
    dil: 'tr'
  },
  {
    mentor_id: 49,
    ad_soyad: 'Mehmet Şahin',
    uzmanlik_alani: 'Veri Bilimi',
    derecelendirme: 4.6,
    deneyim_yili: 6,
    bio_kisa: 'Machine Learning ve veri analizi konusunda uzman. Python, R ve SQL kullanıyor.',
    dil: 'tr'
  },
  {
    mentor_id: 50,
    ad_soyad: 'Elif Yıldız',
    uzmanlik_alani: 'Web Tasarım',
    derecelendirme: 4.8,
    deneyim_yili: 5,
    bio_kisa: 'UI/UX tasarımcı ve frontend geliştirici. React, Vue.js ve modern web teknolojileri konusunda uzman.',
    dil: 'tr'
  },
  {
    mentor_id: 51,
    ad_soyad: 'Can Arslan',
    uzmanlik_alani: 'İşletme ve Girişimcilik',
    derecelendirme: 4.5,
    deneyim_yili: 12,
    bio_kisa: 'İş geliştirme ve girişimcilik konusunda deneyimli mentor. Startup kurma ve yönetimi.',
    dil: 'tr'
  },
  {
    mentor_id: 52,
    ad_soyad: 'Selin Aydın',
    uzmanlik_alani: 'Dijital Pazarlama',
    derecelendirme: 4.7,
    deneyim_yili: 8,
    bio_kisa: 'SEO, SEM ve sosyal medya pazarlama konusunda uzman. Marka yönetimi ve içerik stratejisi.',
    dil: 'tr'
  },
  {
    mentor_id: 53,
    ad_soyad: 'Emre Doğan',
    uzmanlik_alani: 'Finans ve Yatırım',
    derecelendirme: 4.6,
    deneyim_yili: 11,
    bio_kisa: 'Finansal planlama, yatırım stratejileri ve kişisel finans yönetimi konusunda uzman.',
    dil: 'tr'
  }
]);

// Mentor oyları koleksiyonu (simülasyon için - gerçek uygulamada her kullanıcı bir mentora sadece bir kez oy verebilir)
// Bu örnek veriler sadece istatistikler için kullanılıyor
db.mentor_oylari.insertMany([
  { mentor_id: 45, kullanici_id: 101, oy: 5 },
  { mentor_id: 45, kullanici_id: 102, oy: 5 },
  { mentor_id: 45, kullanici_id: 103, oy: 4 },
  { mentor_id: 45, kullanici_id: 104, oy: 5 },
  { mentor_id: 45, kullanici_id: 105, oy: 4 },
  { mentor_id: 46, kullanici_id: 101, oy: 4 },
  { mentor_id: 46, kullanici_id: 102, oy: 5 },
  { mentor_id: 46, kullanici_id: 103, oy: 4 },
  { mentor_id: 46, kullanici_id: 104, oy: 5 },
  { mentor_id: 46, kullanici_id: 105, oy: 4 },
  { mentor_id: 47, kullanici_id: 101, oy: 5 },
  { mentor_id: 47, kullanici_id: 102, oy: 5 },
  { mentor_id: 47, kullanici_id: 103, oy: 5 },
  { mentor_id: 47, kullanici_id: 104, oy: 5 },
  { mentor_id: 47, kullanici_id: 105, oy: 4 },
  { mentor_id: 48, kullanici_id: 101, oy: 5 },
  { mentor_id: 48, kullanici_id: 102, oy: 4 },
  { mentor_id: 48, kullanici_id: 103, oy: 5 },
  { mentor_id: 48, kullanici_id: 104, oy: 4 },
  { mentor_id: 48, kullanici_id: 105, oy: 5 },
  { mentor_id: 49, kullanici_id: 101, oy: 4 },
  { mentor_id: 49, kullanici_id: 102, oy: 5 },
  { mentor_id: 49, kullanici_id: 103, oy: 5 },
  { mentor_id: 49, kullanici_id: 104, oy: 4 },
  { mentor_id: 49, kullanici_id: 105, oy: 5 },
  { mentor_id: 50, kullanici_id: 101, oy: 5 },
  { mentor_id: 50, kullanici_id: 102, oy: 5 },
  { mentor_id: 50, kullanici_id: 103, oy: 4 },
  { mentor_id: 50, kullanici_id: 104, oy: 5 },
  { mentor_id: 50, kullanici_id: 105, oy: 4 },
  { mentor_id: 51, kullanici_id: 101, oy: 4 },
  { mentor_id: 51, kullanici_id: 102, oy: 5 },
  { mentor_id: 51, kullanici_id: 103, oy: 5 },
  { mentor_id: 51, kullanici_id: 104, oy: 5 },
  { mentor_id: 51, kullanici_id: 105, oy: 4 },
  { mentor_id: 52, kullanici_id: 101, oy: 5 },
  { mentor_id: 52, kullanici_id: 102, oy: 4 },
  { mentor_id: 52, kullanici_id: 103, oy: 5 },
  { mentor_id: 52, kullanici_id: 104, oy: 5 },
  { mentor_id: 52, kullanici_id: 105, oy: 4 },
  { mentor_id: 53, kullanici_id: 101, oy: 4 },
  { mentor_id: 53, kullanici_id: 102, oy: 5 },
  { mentor_id: 53, kullanici_id: 103, oy: 4 },
  { mentor_id: 53, kullanici_id: 104, oy: 5 },
  { mentor_id: 53, kullanici_id: 105, oy: 5 }
]);

// İndeksler oluştur
db.kullanicilar.createIndex({ eposta: 1 }, { unique: true });
db.kullanicilar.createIndex({ kullanici_id: 1 }, { unique: true });
db.mentorlar.createIndex({ mentor_id: 1 }, { unique: true });
db.mentorlar.createIndex({ uzmanlik_alani: 1 });
db.mentor_oylari.createIndex({ mentor_id: 1, kullanici_id: 1 }, { unique: true });
db.danismalar.createIndex({ danisma_id: 1 }, { unique: true });
db.danismalar.createIndex({ kullanici_id: 1 });
db.danismalar.createIndex({ mentor_id: 1 });
db.danismalar.createIndex({ durum: 1 });

print('MongoDB başlangıç verileri başarıyla yüklendi!');

