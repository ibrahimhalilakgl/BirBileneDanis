from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sifrekoymaklaugrasmakistememek'

# CORS desteği - Frontend'ten istek yapabilmek için
CORS(app, resources={r"/*": {"origins": "*"}}) 

# In-Memory Veri Yapıları
KULLANICILAR = {
    "mentor@mail.com": {"id": 101, "sifre": "123456", "rol": "mentor", "adSoyad": "Ayşe Demir", "kayitTarihi": "2024-01-15"},
    "kullanici@mail.com": {"id": 102, "sifre": "123456", "rol": "kullanici", "adSoyad": "Ahmet Yılmaz", "kayitTarihi": "2024-02-20"}
}

# Danışma geçmişi için veri yapısı
DANISMA_GECMISI = {}

# Mentor derecelendirmeleri (mentorId -> [oylar])
MENTOR_OYLARI = {
    45: [5, 5, 4, 5, 4],
    46: [4, 5, 4, 5, 4],
    47: [5, 5, 5, 5, 4],
    48: [5, 4, 5, 4, 5],
    49: [4, 5, 5, 4, 5],
    50: [5, 5, 4, 5, 4],
    51: [4, 5, 5, 5, 4],
    52: [5, 4, 5, 5, 4],
    53: [4, 5, 4, 5, 5]
}

# Uzmanlık alanları ve mentorlar
MENTORLAR = [
    # Yazılım Geliştirme
    {
        "mentorId": 45,
        "adSoyad": "Ayşe Demir",
        "uzmanlikAlani": "Yazılım Geliştirme",
        "derecelendirme": 4.8,
        "deneyimYili": 10,
        "bioKisa": "10 yıllık deneyimli tam yığın geliştirici. Python, JavaScript ve Java konusunda uzman.",
        "dil": "tr",
    },
    {
        "mentorId": 47,
        "adSoyad": "Cem Yılmaz",
        "uzmanlikAlani": "Yazılım Geliştirme",
        "derecelendirme": 4.9,
        "deneyimYili": 8,
        "bioKisa": "Bulut mimarileri ve mikroservisler üzerine çalışan mentor.",
        "dil": "en",
    },
    # Kariyer Planlama
    {
        "mentorId": 46,
        "adSoyad": "Burak Kaya",
        "uzmanlikAlani": "Kariyer Planlama",
        "derecelendirme": 4.5,
        "deneyimYili": 7,
        "bioKisa": "Kariyer planlama ve mülakat koçluğu konusunda uzman.",
        "dil": "tr",
    },
    {
        "mentorId": 48,
        "adSoyad": "Zeynep Öztürk",
        "uzmanlikAlani": "Kariyer Planlama",
        "derecelendirme": 4.7,
        "deneyimYili": 9,
        "bioKisa": "HR uzmanı ve kariyer danışmanı. CV hazırlama ve iş görüşmesi teknikleri konusunda deneyimli.",
        "dil": "tr",
    },
    # Veri Bilimi
    {
        "mentorId": 49,
        "adSoyad": "Mehmet Şahin",
        "uzmanlikAlani": "Veri Bilimi",
        "derecelendirme": 4.6,
        "deneyimYili": 6,
        "bioKisa": "Machine Learning ve veri analizi konusunda uzman. Python, R ve SQL kullanıyor.",
        "dil": "tr",
    },
    # Web Tasarım
    {
        "mentorId": 50,
        "adSoyad": "Elif Yıldız",
        "uzmanlikAlani": "Web Tasarım",
        "derecelendirme": 4.8,
        "deneyimYili": 5,
        "bioKisa": "UI/UX tasarımcı ve frontend geliştirici. React, Vue.js ve modern web teknolojileri konusunda uzman.",
        "dil": "tr",
    },
    # İşletme ve Girişimcilik
    {
        "mentorId": 51,
        "adSoyad": "Can Arslan",
        "uzmanlikAlani": "İşletme ve Girişimcilik",
        "derecelendirme": 4.5,
        "deneyimYili": 12,
        "bioKisa": "İş geliştirme ve girişimcilik konusunda deneyimli mentor. Startup kurma ve yönetimi.",
        "dil": "tr",
    },
    # Dijital Pazarlama
    {
        "mentorId": 52,
        "adSoyad": "Selin Aydın",
        "uzmanlikAlani": "Dijital Pazarlama",
        "derecelendirme": 4.7,
        "deneyimYili": 8,
        "bioKisa": "SEO, SEM ve sosyal medya pazarlama konusunda uzman. Marka yönetimi ve içerik stratejisi.",
        "dil": "tr",
    },
    # Finans ve Yatırım
    {
        "mentorId": 53,
        "adSoyad": "Emre Doğan",
        "uzmanlikAlani": "Finans ve Yatırım",
        "derecelendirme": 4.6,
        "deneyimYili": 11,
        "bioKisa": "Finansal planlama, yatırım stratejileri ve kişisel finans yönetimi konusunda uzman.",
        "dil": "tr",
    },
]

# Uzmanlık alanları listesi
UZMANLIK_ALANLARI = list(set([m["uzmanlikAlani"] for m in MENTORLAR]))

# ---------------- Yardımcı Fonksiyonlar ----------------

def jwt_dogrula():
    """JWT token doğrulama helper fonksiyonu"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, jsonify({"hataKodu": "UNAUTHORIZED", "mesaj": "Yetkilendirme tokeni eksik."}), 403
    
    try:
        token = auth_header.split(' ')[1]
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return decoded, None, None
    except jwt.ExpiredSignatureError:
        return None, jsonify({"hataKodu": "FORBIDDEN", "mesaj": "Token süresi dolmuş."}), 403
    except jwt.InvalidTokenError:
        return None, jsonify({"hataKodu": "FORBIDDEN", "mesaj": "Geçersiz yetkilendirme tokeni."}), 403

# ---------------- API Uç Noktaları ----------------

@app.route('/', methods=['GET'])
def health_check():
    """API Sağlık Kontrolü"""
    return jsonify({"message": "Bir Bilene Danış API'si hazır!"}), 200

@app.route('/kullanici/giris', methods=['POST'])
def kullanici_giris():
    """Kullanıcı Girişi"""
    data = request.get_json()
    eposta = data.get('eposta')
    sifre = data.get('sifre')

    if eposta in KULLANICILAR and KULLANICILAR[eposta]['sifre'] == sifre:
        # JWT Token Oluşturma
        token_payload = {
            'user_id': KULLANICILAR[eposta]['id'],
            'rol': KULLANICILAR[eposta]['rol'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            "durum": "basarili",
            "token": token
        }), 200
    else:
        return jsonify({
            "hataKodu": "AUTH_FAILED",
            "mesaj": "Geçersiz e-posta veya şifre."
        }), 401

@app.route('/mentor/ara', methods=['GET'])
def mentor_ara():
    """Mentor Arama ve Filtreleme"""
    alan = request.args.get('alan')
    dil = request.args.get('dil')  # Opsiyonel

    if not alan:
        return jsonify({"hataKodu": "BAD_REQUEST", "mesaj": "Alan parametresi gereklidir."}), 400

    eslesen_mentorlar = [
        m for m in MENTORLAR
        if alan.lower() in m['uzmanlikAlani'].lower()
        and (dil is None or m.get("dil", "tr") == dil)
    ]

    if not eslesen_mentorlar:
        return jsonify({"hataKodu": "NOT_FOUND", "mesaj": f"'{alan}' alanında mentor bulunamadı."}), 404

    return jsonify(eslesen_mentorlar), 200

@app.route('/danisma/gonder', methods=['POST'])
def danisma_gonder():
    """Danışma Sorusu Gönderimi (Token doğrulama simülasyonu)"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code

    #Yetkilendirme başarılı, danışma işlemini simüle et
    data = request.get_json()
    mentor_id = data.get('mentorId')
    soru_basligi = data.get('soruBasligi', '')
    soru_icerigi = data.get('soruIcerigi', '')

    #Mentor var mı kontrolü
    mentor_var = any(m['mentorId'] == mentor_id for m in MENTORLAR)
    if not mentor_var:
        return jsonify({"hataKodu": "NOT_FOUND", "mesaj": f"Mentor ID: {mentor_id} bulunamadı."}), 404

    # Danışma kaydı oluştur
    danisma_id = f"DS-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    user_id = decoded['user_id']
    
    DANISMA_GECMISI[danisma_id] = {
        "danismaId": danisma_id,
        "kullaniciId": user_id,
        "mentorId": mentor_id,
        "soruBasligi": soru_basligi,
        "soruIcerigi": soru_icerigi,
        "durum": "beklemede",
        "tarih": datetime.datetime.now().isoformat()
    }

    return jsonify({
        "durum": "basarili",
        "danismaId": danisma_id,
        "mesaj": "Sorunuz mentora iletilmiştir. Yanıt geldiğinde bildirim alacaksınız."
    }), 201

@app.route('/uzmanlik/alanlar', methods=['GET'])
def uzmanlik_alanlari():
    """Tüm uzmanlık alanlarını listeleme"""
    return jsonify({
        "alanlar": sorted(UZMANLIK_ALANLARI)
    }), 200

@app.route('/mentor/liste', methods=['GET'])
def mentor_liste():
    """Tüm mentorları listeleme"""
    return jsonify({
        "toplam": len(MENTORLAR),
        "mentorlar": MENTORLAR
    }), 200

@app.route('/mentor/<int:mentor_id>', methods=['GET'])
def mentor_detay(mentor_id):
    """Belirli bir mentorun detaylarını getirme"""
    mentor = next((m for m in MENTORLAR if m['mentorId'] == mentor_id), None)
    
    if not mentor:
        return jsonify({
            "hataKodu": "NOT_FOUND",
            "mesaj": f"Mentor ID: {mentor_id} bulunamadı."
        }), 404
    
    # Mentor oylarını hesapla
    oylar = MENTOR_OYLARI.get(mentor_id, [])
    ortalama_oy = sum(oylar) / len(oylar) if oylar else mentor.get('derecelendirme', 0)
    
    mentor_detay = mentor.copy()
    mentor_detay['toplamOy'] = len(oylar)
    mentor_detay['hesaplananDerecelendirme'] = round(ortalama_oy, 1)
    
    return jsonify(mentor_detay), 200

@app.route('/kullanici/profil', methods=['GET'])
def kullanici_profil():
    """Kullanıcı profil bilgilerini getirme"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    user_id = decoded['user_id']
    kullanici = next((k for k in KULLANICILAR.values() if k['id'] == user_id), None)
    
    if not kullanici:
        return jsonify({
            "hataKodu": "NOT_FOUND",
            "mesaj": "Kullanıcı bulunamadı."
        }), 404
    
    # Kullanıcının danışma geçmişini getir
    kullanici_danismalari = [
        d for d in DANISMA_GECMISI.values()
        if d['kullaniciId'] == user_id
    ]
    
    return jsonify({
        "kullaniciId": kullanici['id'],
        "adSoyad": kullanici.get('adSoyad', ''),
        "rol": kullanici['rol'],
        "kayitTarihi": kullanici.get('kayitTarihi', ''),
        "toplamDanisma": len(kullanici_danismalari),
        "danismaGecmisi": kullanici_danismalari
    }), 200

@app.route('/danisma/gecmis', methods=['GET'])
def danisma_gecmis():
    """Kullanıcının danışma geçmişini görüntüleme"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    user_id = decoded['user_id']
    kullanici_danismalari = [
        d for d in DANISMA_GECMISI.values()
        if d['kullaniciId'] == user_id
    ]
    
    return jsonify({
        "toplam": len(kullanici_danismalari),
        "danismalar": kullanici_danismalari
    }), 200

@app.route('/danisma/<danisma_id>', methods=['GET'])
def danisma_durum(danisma_id):
    """Belirli bir danışmanın durumunu sorgulama"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    danisma = DANISMA_GECMISI.get(danisma_id)
    
    if not danisma:
        return jsonify({
            "hataKodu": "NOT_FOUND",
            "mesaj": f"Danışma ID: {danisma_id} bulunamadı."
        }), 404
    
    # Kullanıcı kendi danışmasını mı sorguluyor kontrol et
    user_id = decoded['user_id']
    if danisma['kullaniciId'] != user_id:
        return jsonify({
            "hataKodu": "FORBIDDEN",
            "mesaj": "Bu danışmaya erişim yetkiniz yok."
        }), 403
    
    return jsonify(danisma), 200

@app.route('/mentor/<int:mentor_id>/oyla', methods=['POST'])
def mentor_oyla(mentor_id):
    """Mentora oy verme/derecelendirme"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    mentor = next((m for m in MENTORLAR if m['mentorId'] == mentor_id), None)
    if not mentor:
        return jsonify({
            "hataKodu": "NOT_FOUND",
            "mesaj": f"Mentor ID: {mentor_id} bulunamadı."
        }), 404
    
    data = request.get_json()
    oy = data.get('oy')
    
    if not oy or not isinstance(oy, (int, float)) or oy < 1 or oy > 5:
        return jsonify({
            "hataKodu": "BAD_REQUEST",
            "mesaj": "Oy değeri 1 ile 5 arasında olmalıdır."
        }), 400
    
    # Oy kaydet
    if mentor_id not in MENTOR_OYLARI:
        MENTOR_OYLARI[mentor_id] = []
    
    MENTOR_OYLARI[mentor_id].append(int(oy))
    
    # Yeni ortalamayı hesapla
    oylar = MENTOR_OYLARI[mentor_id]
    yeni_ortalama = sum(oylar) / len(oylar)
    
    return jsonify({
        "durum": "basarili",
        "mesaj": "Oy başarıyla kaydedildi.",
        "mentorId": mentor_id,
        "verilenOy": int(oy),
        "toplamOy": len(oylar),
        "yeniOrtalama": round(yeni_ortalama, 1)
    }), 200

@app.route('/kullanici/kayit', methods=['POST'])
def kullanici_kayit():
    """Yeni kullanıcı kaydı"""
    data = request.get_json()
    eposta = data.get('eposta')
    sifre = data.get('sifre')
    ad_soyad = data.get('adSoyad', '')
    
    if not eposta or not sifre:
        return jsonify({
            "hataKodu": "BAD_REQUEST",
            "mesaj": "E-posta ve şifre gereklidir."
        }), 400
    
    if eposta in KULLANICILAR:
        return jsonify({
            "hataKodu": "CONFLICT",
            "mesaj": "Bu e-posta adresi zaten kayıtlı."
        }), 409
    
    # Yeni kullanıcı ID'si oluştur
    yeni_id = max([k['id'] for k in KULLANICILAR.values()], default=100) + 1
    
    KULLANICILAR[eposta] = {
        "id": yeni_id,
        "sifre": sifre,
        "rol": "kullanici",
        "adSoyad": ad_soyad,
        "kayitTarihi": datetime.datetime.now().strftime('%Y-%m-%d')
    }
    
    return jsonify({
        "durum": "basarili",
        "mesaj": "Kullanıcı başarıyla kaydedildi.",
        "kullaniciId": yeni_id
    }), 201

@app.route('/istatistikler', methods=['GET'])
def istatistikler():
    """Genel platform istatistikleri"""
    return jsonify({
        "toplamMentor": len(MENTORLAR),
        "toplamKullanici": len(KULLANICILAR),
        "toplamDanisma": len(DANISMA_GECMISI),
        "bekleyenDanisma": len([d for d in DANISMA_GECMISI.values() if d['durum'] == 'beklemede']),
        "enPopulerMentor": max(MENTORLAR, key=lambda m: len(MENTOR_OYLARI.get(m['mentorId'], []))).get('adSoyad', '') if MENTORLAR else None
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
