from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
import datetime
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from bson import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sifrekoymaklaugrasmakistememek'

# CORS desteği - Frontend'ten istek yapabilmek için
CORS(app, resources={r"/*": {"origins": "*"}}) 

# MongoDB Bağlantı Ayarları
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://admin:admin123@mongodb:27017/birbilenedanis?authSource=admin')
MONGODB_DB = os.getenv('MONGODB_DB', 'birbilenedanis')

# MongoDB Client
mongo_client = None
db = None

def get_db():
    """MongoDB veritabanı bağlantısı al"""
    global mongo_client, db
    if mongo_client is None:
        try:
            mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            db = mongo_client[MONGODB_DB]
            # Bağlantıyı test et
            mongo_client.admin.command('ping')
            return db
        except ConnectionFailure as e:
            print(f"MongoDB bağlantı hatası: {e}")
            return None
    return db

def init_db():
    """MongoDB bağlantısını test et"""
    try:
        database = get_db()
        if database:
            database.admin.command('ping')
            return True
    except Exception as e:
        print(f"Veritabanı başlatma hatası: {e}")
    return False

# Uygulama başlangıcında veritabanını kontrol et
with app.app_context():
    if not init_db():
        print("Uyarı: MongoDB bağlantısı kurulamadı. Lütfen docker-compose.mongodb.yml ile servisleri başlatın.")

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
    database = get_db()
    if database:
        try:
            database.admin.command('ping')
            return jsonify({"message": "Bir Bilene Danış API'si hazır!", "database": "connected"}), 200
        except:
            pass
    return jsonify({"message": "Bir Bilene Danış API'si hazır!", "database": "disconnected"}), 200

@app.route('/kullanici/giris', methods=['POST'])
def kullanici_giris():
    """Kullanıcı Girişi"""
    data = request.get_json()
    eposta = data.get('eposta')
    sifre = data.get('sifre')

    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        kullanici = database.kullanicilar.find_one({"eposta": eposta})
        
        if kullanici and kullanici.get('sifre') == sifre:
            # JWT Token Oluşturma
            token_payload = {
                'user_id': kullanici['kullanici_id'],
                'rol': kullanici['rol'],
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
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/mentor/ara', methods=['GET'])
def mentor_ara():
    """Mentor Arama ve Filtreleme"""
    alan = request.args.get('alan')
    dil = request.args.get('dil')  # Opsiyonel

    if not alan:
        return jsonify({"hataKodu": "BAD_REQUEST", "mesaj": "Alan parametresi gereklidir."}), 400

    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        query = {"uzmanlik_alani": {"$regex": alan, "$options": "i"}}
        if dil:
            query["dil"] = dil
        
        mentorlar = list(database.mentorlar.find(query))
        
        if not mentorlar:
            return jsonify({"hataKodu": "NOT_FOUND", "mesaj": f"'{alan}' alanında mentor bulunamadı."}), 404

        # Dictionary formatına çevir
        result = []
        for m in mentorlar:
            result.append({
                "mentorId": m['mentor_id'],
                "adSoyad": m['ad_soyad'],
                "uzmanlikAlani": m['uzmanlik_alani'],
                "derecelendirme": float(m.get('derecelendirme', 0)) if m.get('derecelendirme') else None,
                "deneyimYili": m.get('deneyim_yili', 0),
                "bioKisa": m.get('bio_kisa', ''),
                "dil": m.get('dil', 'tr')
            })

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/danisma/gonder', methods=['POST'])
def danisma_gonder():
    """Danışma Sorusu Gönderimi"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code

    data = request.get_json()
    mentor_id = data.get('mentorId')
    soru_basligi = data.get('soruBasligi', '')
    soru_icerigi = data.get('soruIcerigi', '')

    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        # Mentor var mı kontrolü
        mentor = database.mentorlar.find_one({"mentor_id": mentor_id})
        
        if not mentor:
            return jsonify({"hataKodu": "NOT_FOUND", "mesaj": f"Mentor ID: {mentor_id} bulunamadı."}), 404

        # Danışma kaydı oluştur
        danisma_id = f"DS-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        user_id = decoded['user_id']
        
        danisma_doc = {
            "danisma_id": danisma_id,
            "kullanici_id": user_id,
            "mentor_id": mentor_id,
            "soru_basligi": soru_basligi,
            "soru_icerigi": soru_icerigi,
            "durum": "beklemede",
            "olusturma_tarihi": datetime.datetime.now()
        }
        
        database.danismalar.insert_one(danisma_doc)

        return jsonify({
            "durum": "basarili",
            "danismaId": danisma_id,
            "mesaj": "Sorunuz mentora iletilmiştir. Yanıt geldiğinde bildirim alacaksınız."
        }), 201
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/uzmanlik/alanlar', methods=['GET'])
def uzmanlik_alanlari():
    """Tüm uzmanlık alanlarını listeleme"""
    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        alanlar = database.mentorlar.distinct("uzmanlik_alani")
        return jsonify({
            "alanlar": sorted(alanlar)
        }), 200
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/mentor/liste', methods=['GET'])
def mentor_liste():
    """Tüm mentorları listeleme"""
    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        mentorlar = list(database.mentorlar.find().sort("mentor_id", 1))
        
        result = []
        for m in mentorlar:
            result.append({
                "mentorId": m['mentor_id'],
                "adSoyad": m['ad_soyad'],
                "uzmanlikAlani": m['uzmanlik_alani'],
                "derecelendirme": float(m.get('derecelendirme', 0)) if m.get('derecelendirme') else None,
                "deneyimYili": m.get('deneyim_yili', 0),
                "bioKisa": m.get('bio_kisa', ''),
                "dil": m.get('dil', 'tr')
            })

        return jsonify({
            "toplam": len(result),
            "mentorlar": result
        }), 200
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/mentor/<int:mentor_id>', methods=['GET'])
def mentor_detay(mentor_id):
    """Belirli bir mentorun detaylarını getirme"""
    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        mentor = database.mentorlar.find_one({"mentor_id": mentor_id})
        
        if not mentor:
            return jsonify({
                "hataKodu": "NOT_FOUND",
                "mesaj": f"Mentor ID: {mentor_id} bulunamadı."
            }), 404
        
        # Mentor oylarını hesapla
        oylar = list(database.mentor_oylari.find({"mentor_id": mentor_id}))
        oy_degerleri = [oy['oy'] for oy in oylar]
        ortalama_oy = sum(oy_degerleri) / len(oy_degerleri) if oy_degerleri else mentor.get('derecelendirme', 0)
        toplam_oy = len(oy_degerleri)
        
        mentor_detay = {
            "mentorId": mentor['mentor_id'],
            "adSoyad": mentor['ad_soyad'],
            "uzmanlikAlani": mentor['uzmanlik_alani'],
            "derecelendirme": float(mentor.get('derecelendirme', 0)) if mentor.get('derecelendirme') else None,
            "deneyimYili": mentor.get('deneyim_yili', 0),
            "bioKisa": mentor.get('bio_kisa', ''),
            "dil": mentor.get('dil', 'tr'),
            "toplamOy": toplam_oy,
            "hesaplananDerecelendirme": round(ortalama_oy, 1) if ortalama_oy else None
        }
        
        return jsonify(mentor_detay), 200
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/kullanici/profil', methods=['GET'])
def kullanici_profil():
    """Kullanıcı profil bilgilerini getirme"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    user_id = decoded['user_id']
    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        kullanici = database.kullanicilar.find_one({"kullanici_id": user_id})
        
        if not kullanici:
            return jsonify({
                "hataKodu": "NOT_FOUND",
                "mesaj": "Kullanıcı bulunamadı."
            }), 404
        
        # Kullanıcının danışma geçmişini getir
        danismalar = list(database.danismalar.find({"kullanici_id": user_id}).sort("olusturma_tarihi", -1))
        
        danisma_gecmisi = []
        for d in danismalar:
            danisma_gecmisi.append({
                "danismaId": d['danisma_id'],
                "kullaniciId": d['kullanici_id'],
                "mentorId": d['mentor_id'],
                "soruBasligi": d.get('soru_basligi', ''),
                "soruIcerigi": d.get('soru_icerigi', ''),
                "durum": d.get('durum', 'beklemede'),
                "tarih": d.get('olusturma_tarihi').isoformat() if d.get('olusturma_tarihi') else None
            })
        
        return jsonify({
            "kullaniciId": kullanici['kullanici_id'],
            "adSoyad": kullanici.get('ad_soyad', ''),
            "rol": kullanici['rol'],
            "kayitTarihi": kullanici.get('kayit_tarihi', ''),
            "toplamDanisma": len(danisma_gecmisi),
            "danismaGecmisi": danisma_gecmisi
        }), 200
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/danisma/gecmis', methods=['GET'])
def danisma_gecmis():
    """Kullanıcının danışma geçmişini görüntüleme"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    user_id = decoded['user_id']
    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        danismalar = list(database.danismalar.find({"kullanici_id": user_id}).sort("olusturma_tarihi", -1))
        
        result = []
        for d in danismalar:
            result.append({
                "danismaId": d['danisma_id'],
                "kullaniciId": d['kullanici_id'],
                "mentorId": d['mentor_id'],
                "soruBasligi": d.get('soru_basligi', ''),
                "soruIcerigi": d.get('soru_icerigi', ''),
                "durum": d.get('durum', 'beklemede'),
                "tarih": d.get('olusturma_tarihi').isoformat() if d.get('olusturma_tarihi') else None
            })
        
        return jsonify({
            "toplam": len(result),
            "danismalar": result
        }), 200
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/danisma/<danisma_id>', methods=['GET'])
def danisma_durum(danisma_id):
    """Belirli bir danışmanın durumunu sorgulama"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        danisma = database.danismalar.find_one({"danisma_id": danisma_id})
        
        if not danisma:
            return jsonify({
                "hataKodu": "NOT_FOUND",
                "mesaj": f"Danışma ID: {danisma_id} bulunamadı."
            }), 404
        
        # Kullanıcı kendi danışmasını mı sorguluyor kontrol et
        user_id = decoded['user_id']
        if danisma['kullanici_id'] != user_id:
            return jsonify({
                "hataKodu": "FORBIDDEN",
                "mesaj": "Bu danışmaya erişim yetkiniz yok."
            }), 403
        
        result = {
            "danismaId": danisma['danisma_id'],
            "kullaniciId": danisma['kullanici_id'],
            "mentorId": danisma['mentor_id'],
            "soruBasligi": danisma.get('soru_basligi', ''),
            "soruIcerigi": danisma.get('soru_icerigi', ''),
            "durum": danisma.get('durum', 'beklemede'),
            "tarih": danisma.get('olusturma_tarihi').isoformat() if danisma.get('olusturma_tarihi') else None
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/mentor/<int:mentor_id>/oyla', methods=['POST'])
def mentor_oyla(mentor_id):
    """Mentora oy verme/derecelendirme"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        # Mentor var mı kontrol et
        mentor = database.mentorlar.find_one({"mentor_id": mentor_id})
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
        
        user_id = decoded['user_id']
        
        # Oy kaydet (eğer daha önce oy vermişse güncelle)
        database.mentor_oylari.update_one(
            {"mentor_id": mentor_id, "kullanici_id": user_id},
            {
                "$set": {
                    "oy": int(oy),
                    "olusturma_tarihi": datetime.datetime.now()
                }
            },
            upsert=True
        )
        
        # Yeni ortalamayı hesapla
        oylar = list(database.mentor_oylari.find({"mentor_id": mentor_id}))
        oy_degerleri = [oy['oy'] for oy in oylar]
        yeni_ortalama = sum(oy_degerleri) / len(oy_degerleri) if oy_degerleri else 0
        toplam_oy = len(oy_degerleri)
        
        return jsonify({
            "durum": "basarili",
            "mesaj": "Oy başarıyla kaydedildi.",
            "mentorId": mentor_id,
            "verilenOy": int(oy),
            "toplamOy": toplam_oy,
            "yeniOrtalama": round(yeni_ortalama, 1)
        }), 200
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

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
    
    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        # E-posta kontrolü
        if database.kullanicilar.find_one({"eposta": eposta}):
            return jsonify({
                "hataKodu": "CONFLICT",
                "mesaj": "Bu e-posta adresi zaten kayıtlı."
            }), 409
        
        # Yeni kullanıcı ID'si oluştur
        son_kullanici = database.kullanicilar.find_one(sort=[("kullanici_id", -1)])
        yeni_id = (son_kullanici['kullanici_id'] if son_kullanici else 100) + 1
        
        # Yeni kullanıcı ekle
        yeni_kullanici = {
            "kullanici_id": yeni_id,
            "eposta": eposta,
            "sifre": sifre,
            "rol": "kullanici",
            "ad_soyad": ad_soyad,
            "kayit_tarihi": datetime.datetime.now().strftime('%Y-%m-%d')
        }
        
        database.kullanicilar.insert_one(yeni_kullanici)
        
        return jsonify({
            "durum": "basarili",
            "mesaj": "Kullanıcı başarıyla kaydedildi.",
            "kullaniciId": yeni_id
        }), 201
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/istatistikler', methods=['GET'])
def istatistikler():
    """Genel platform istatistikleri"""
    database = get_db()
    if not database:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        # Toplam mentor sayısı
        toplam_mentor = database.mentorlar.count_documents({})
        
        # Toplam kullanıcı sayısı
        toplam_kullanici = database.kullanicilar.count_documents({})
        
        # Toplam danışma sayısı
        toplam_danisma = database.danismalar.count_documents({})
        
        # Bekleyen danışma sayısı
        bekleyen_danisma = database.danismalar.count_documents({"durum": "beklemede"})
        
        # En popüler mentor (en çok oy alan)
        pipeline = [
            {"$group": {
                "_id": "$mentor_id",
                "oy_sayisi": {"$sum": 1}
            }},
            {"$sort": {"oy_sayisi": -1}},
            {"$limit": 1}
        ]
        en_populer_oy = list(database.mentor_oylari.aggregate(pipeline))
        
        en_populer_mentor = None
        if en_populer_oy:
            mentor_id = en_populer_oy[0]['_id']
            mentor = database.mentorlar.find_one({"mentor_id": mentor_id})
            if mentor:
                en_populer_mentor = mentor.get('ad_soyad')
        
        return jsonify({
            "toplamMentor": toplam_mentor,
            "toplamKullanici": toplam_kullanici,
            "toplamDanisma": toplam_danisma,
            "bekleyenDanisma": bekleyen_danisma,
            "enPopulerMentor": en_populer_mentor
        }), 200
    except Exception as e:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

