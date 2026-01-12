from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import jwt
import datetime
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sifrekoymaklaugrasmakistememek'

# CORS desteği - Frontend'ten istek yapabilmek için
CORS(app, resources={r"/*": {"origins": "*"}}) 

# PostgreSQL Bağlantı Ayarları
DATABASE_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'postgres'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'birbilenedanis'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres123')
}

# Connection Pool Oluştur
connection_pool = None

def get_db_connection():
    """Veritabanı bağlantısı al"""
    global connection_pool
    if connection_pool is None:
        try:
            connection_pool = SimpleConnectionPool(1, 20, **DATABASE_CONFIG)
        except Exception as e:
            print(f"Veritabanı bağlantı hatası: {e}")
            return None
    
    try:
        return connection_pool.getconn()
    except Exception as e:
        print(f"Bağlantı alma hatası: {e}")
        return None

def return_db_connection(conn):
    """Veritabanı bağlantısını pool'a geri ver"""
    if connection_pool and conn:
        connection_pool.putconn(conn)

def init_db():
    """Veritabanı bağlantısını test et ve gerekirse tabloları oluştur"""
    conn = get_db_connection()
    if conn:
        return_db_connection(conn)
        return True
    return False

# Uygulama başlangıcında veritabanını kontrol et
with app.app_context():
    if not init_db():
        print("Uyarı: Veritabanı bağlantısı kurulamadı. Lütfen docker-compose.yml ile servisleri başlatın.")

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
    conn = get_db_connection()
    if conn:
        return_db_connection(conn)
        return jsonify({"message": "Bir Bilene Danış API'si hazır!", "database": "connected"}), 200
    return jsonify({"message": "Bir Bilene Danış API'si hazır!", "database": "disconnected"}), 200

@app.route('/kullanici/giris', methods=['POST'])
def kullanici_giris():
    """Kullanıcı Girişi"""
    data = request.get_json()
    eposta = data.get('eposta')
    sifre = data.get('sifre')

    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT kullanici_id, eposta, sifre, rol, ad_soyad, kayit_tarihi FROM kullanicilar WHERE eposta = %s", (eposta,))
        kullanici = cur.fetchone()
        cur.close()

        if kullanici and kullanici['sifre'] == sifre:
            # JWT Token Oluşturma
            token_payload = {
                'user_id': kullanici['kullanici_id'],
                'rol': kullanici['rol'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
            
            return_db_connection(conn)
            return jsonify({
                "durum": "basarili",
                "token": token
            }), 200
        else:
            return_db_connection(conn)
            return jsonify({
                "hataKodu": "AUTH_FAILED",
                "mesaj": "Geçersiz e-posta veya şifre."
            }), 401
    except Exception as e:
        return_db_connection(conn)
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/mentor/ara', methods=['GET'])
def mentor_ara():
    """Mentor Arama ve Filtreleme"""
    alan = request.args.get('alan')
    dil = request.args.get('dil')  # Opsiyonel

    if not alan:
        return jsonify({"hataKodu": "BAD_REQUEST", "mesaj": "Alan parametresi gereklidir."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        if dil:
            cur.execute("""
                SELECT mentor_id, ad_soyad, uzmanlik_alani, derecelendirme, 
                       deneyim_yili, bio_kisa, dil
                FROM mentorlar 
                WHERE LOWER(uzmanlik_alani) LIKE LOWER(%s) AND dil = %s
            """, (f'%{alan}%', dil))
        else:
            cur.execute("""
                SELECT mentor_id, ad_soyad, uzmanlik_alani, derecelendirme, 
                       deneyim_yili, bio_kisa, dil
                FROM mentorlar 
                WHERE LOWER(uzmanlik_alani) LIKE LOWER(%s)
            """, (f'%{alan}%',))
        
        mentorlar = cur.fetchall()
        cur.close()
        return_db_connection(conn)

        if not mentorlar:
            return jsonify({"hataKodu": "NOT_FOUND", "mesaj": f"'{alan}' alanında mentor bulunamadı."}), 404

        # Dictionary formatına çevir
        result = []
        for m in mentorlar:
            result.append({
                "mentorId": m['mentor_id'],
                "adSoyad": m['ad_soyad'],
                "uzmanlikAlani": m['uzmanlik_alani'],
                "derecelendirme": float(m['derecelendirme']) if m['derecelendirme'] else None,
                "deneyimYili": m['deneyim_yili'],
                "bioKisa": m['bio_kisa'],
                "dil": m['dil']
            })

        return jsonify(result), 200
    except Exception as e:
        return_db_connection(conn)
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/danisma/gonder', methods=['POST'])
def danisma_gonder():
    """Danışma Sorusu Gönderimi (Token doğrulama simülasyonu)"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code

    data = request.get_json()
    mentor_id = data.get('mentorId')
    soru_basligi = data.get('soruBasligi', '')
    soru_icerigi = data.get('soruIcerigi', '')

    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Mentor var mı kontrolü
        cur.execute("SELECT mentor_id FROM mentorlar WHERE mentor_id = %s", (mentor_id,))
        mentor = cur.fetchone()
        
        if not mentor:
            cur.close()
            return_db_connection(conn)
            return jsonify({"hataKodu": "NOT_FOUND", "mesaj": f"Mentor ID: {mentor_id} bulunamadı."}), 404

        # Danışma kaydı oluştur
        danisma_id = f"DS-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        user_id = decoded['user_id']
        
        cur.execute("""
            INSERT INTO danismalar (danisma_id, kullanici_id, mentor_id, soru_basligi, soru_icerigi, durum)
            VALUES (%s, %s, %s, %s, %s, 'beklemede')
            RETURNING danisma_id, olusturma_tarihi
        """, (danisma_id, user_id, mentor_id, soru_basligi, soru_icerigi))
        
        conn.commit()
        cur.close()
        return_db_connection(conn)

        return jsonify({
            "durum": "basarili",
            "danismaId": danisma_id,
            "mesaj": "Sorunuz mentora iletilmiştir. Yanıt geldiğinde bildirim alacaksınız."
        }), 201
    except Exception as e:
        if conn:
            conn.rollback()
            return_db_connection(conn)
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/uzmanlik/alanlar', methods=['GET'])
def uzmanlik_alanlari():
    """Tüm uzmanlık alanlarını listeleme"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT uzmanlik_alani FROM mentorlar ORDER BY uzmanlik_alani")
        alanlar = [row[0] for row in cur.fetchall()]
        cur.close()
        return_db_connection(conn)
        
        return jsonify({
            "alanlar": sorted(alanlar)
        }), 200
    except Exception as e:
        return_db_connection(conn)
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/mentor/liste', methods=['GET'])
def mentor_liste():
    """Tüm mentorları listeleme"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT mentor_id, ad_soyad, uzmanlik_alani, derecelendirme, 
                   deneyim_yili, bio_kisa, dil
            FROM mentorlar
            ORDER BY mentor_id
        """)
        mentorlar = cur.fetchall()
        cur.close()
        return_db_connection(conn)

        result = []
        for m in mentorlar:
            result.append({
                "mentorId": m['mentor_id'],
                "adSoyad": m['ad_soyad'],
                "uzmanlikAlani": m['uzmanlik_alani'],
                "derecelendirme": float(m['derecelendirme']) if m['derecelendirme'] else None,
                "deneyimYili": m['deneyim_yili'],
                "bioKisa": m['bio_kisa'],
                "dil": m['dil']
            })

        return jsonify({
            "toplam": len(result),
            "mentorlar": result
        }), 200
    except Exception as e:
        return_db_connection(conn)
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/mentor/<int:mentor_id>', methods=['GET'])
def mentor_detay(mentor_id):
    """Belirli bir mentorun detaylarını getirme"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT mentor_id, ad_soyad, uzmanlik_alani, derecelendirme, 
                   deneyim_yili, bio_kisa, dil
            FROM mentorlar 
            WHERE mentor_id = %s
        """, (mentor_id,))
        mentor = cur.fetchone()
        
        if not mentor:
            cur.close()
            return_db_connection(conn)
            return jsonify({
                "hataKodu": "NOT_FOUND",
                "mesaj": f"Mentor ID: {mentor_id} bulunamadı."
            }), 404
        
        # Mentor oylarını hesapla
        cur.execute("""
            SELECT AVG(oy) as ortalama, COUNT(*) as toplam
            FROM mentor_oylari
            WHERE mentor_id = %s
        """, (mentor_id,))
        oy_istatistik = cur.fetchone()
        cur.close()
        return_db_connection(conn)
        
        ortalama_oy = float(oy_istatistik['ortalama']) if oy_istatistik['ortalama'] else mentor['derecelendirme']
        toplam_oy = oy_istatistik['toplam'] if oy_istatistik['toplam'] else 0
        
        mentor_detay = {
            "mentorId": mentor['mentor_id'],
            "adSoyad": mentor['ad_soyad'],
            "uzmanlikAlani": mentor['uzmanlik_alani'],
            "derecelendirme": float(mentor['derecelendirme']) if mentor['derecelendirme'] else None,
            "deneyimYili": mentor['deneyim_yili'],
            "bioKisa": mentor['bio_kisa'],
            "dil": mentor['dil'],
            "toplamOy": toplam_oy,
            "hesaplananDerecelendirme": round(ortalama_oy, 1) if ortalama_oy else None
        }
        
        return jsonify(mentor_detay), 200
    except Exception as e:
        return_db_connection(conn)
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/kullanici/profil', methods=['GET'])
def kullanici_profil():
    """Kullanıcı profil bilgilerini getirme"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    user_id = decoded['user_id']
    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT kullanici_id, eposta, rol, ad_soyad, kayit_tarihi
            FROM kullanicilar 
            WHERE kullanici_id = %s
        """, (user_id,))
        kullanici = cur.fetchone()
        
        if not kullanici:
            cur.close()
            return_db_connection(conn)
            return jsonify({
                "hataKodu": "NOT_FOUND",
                "mesaj": "Kullanıcı bulunamadı."
            }), 404
        
        # Kullanıcının danışma geçmişini getir
        cur.execute("""
            SELECT danisma_id, kullanici_id, mentor_id, soru_basligi, soru_icerigi, durum, olusturma_tarihi
            FROM danismalar
            WHERE kullanici_id = %s
            ORDER BY olusturma_tarihi DESC
        """, (user_id,))
        danismalar = cur.fetchall()
        cur.close()
        return_db_connection(conn)
        
        danisma_gecmisi = []
        for d in danismalar:
            danisma_gecmisi.append({
                "danismaId": d['danisma_id'],
                "kullaniciId": d['kullanici_id'],
                "mentorId": d['mentor_id'],
                "soruBasligi": d['soru_basligi'],
                "soruIcerigi": d['soru_icerigi'],
                "durum": d['durum'],
                "tarih": d['olusturma_tarihi'].isoformat() if d['olusturma_tarihi'] else None
            })
        
        return jsonify({
            "kullaniciId": kullanici['kullanici_id'],
            "adSoyad": kullanici.get('ad_soyad', ''),
            "rol": kullanici['rol'],
            "kayitTarihi": kullanici['kayit_tarihi'].strftime('%Y-%m-%d') if kullanici['kayit_tarihi'] else '',
            "toplamDanisma": len(danisma_gecmisi),
            "danismaGecmisi": danisma_gecmisi
        }), 200
    except Exception as e:
        return_db_connection(conn)
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/danisma/gecmis', methods=['GET'])
def danisma_gecmis():
    """Kullanıcının danışma geçmişini görüntüleme"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    user_id = decoded['user_id']
    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT danisma_id, kullanici_id, mentor_id, soru_basligi, soru_icerigi, durum, olusturma_tarihi
            FROM danismalar
            WHERE kullanici_id = %s
            ORDER BY olusturma_tarihi DESC
        """, (user_id,))
        danismalar = cur.fetchall()
        cur.close()
        return_db_connection(conn)
        
        result = []
        for d in danismalar:
            result.append({
                "danismaId": d['danisma_id'],
                "kullaniciId": d['kullanici_id'],
                "mentorId": d['mentor_id'],
                "soruBasligi": d['soru_basligi'],
                "soruIcerigi": d['soru_icerigi'],
                "durum": d['durum'],
                "tarih": d['olusturma_tarihi'].isoformat() if d['olusturma_tarihi'] else None
            })
        
        return jsonify({
            "toplam": len(result),
            "danismalar": result
        }), 200
    except Exception as e:
        return_db_connection(conn)
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/danisma/<danisma_id>', methods=['GET'])
def danisma_durum(danisma_id):
    """Belirli bir danışmanın durumunu sorgulama"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT danisma_id, kullanici_id, mentor_id, soru_basligi, soru_icerigi, durum, olusturma_tarihi
            FROM danismalar
            WHERE danisma_id = %s
        """, (danisma_id,))
        danisma = cur.fetchone()
        cur.close()
        return_db_connection(conn)
        
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
            "soruBasligi": danisma['soru_basligi'],
            "soruIcerigi": danisma['soru_icerigi'],
            "durum": danisma['durum'],
            "tarih": danisma['olusturma_tarihi'].isoformat() if danisma['olusturma_tarihi'] else None
        }
        
        return jsonify(result), 200
    except Exception as e:
        return_db_connection(conn)
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/mentor/<int:mentor_id>/oyla', methods=['POST'])
def mentor_oyla(mentor_id):
    """Mentora oy verme/derecelendirme"""
    decoded, error_response, error_code = jwt_dogrula()
    if error_response:
        return error_response, error_code
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Mentor var mı kontrol et
        cur.execute("SELECT mentor_id FROM mentorlar WHERE mentor_id = %s", (mentor_id,))
        mentor = cur.fetchone()
        if not mentor:
            cur.close()
            return_db_connection(conn)
            return jsonify({
                "hataKodu": "NOT_FOUND",
                "mesaj": f"Mentor ID: {mentor_id} bulunamadı."
            }), 404
        
        data = request.get_json()
        oy = data.get('oy')
        
        if not oy or not isinstance(oy, (int, float)) or oy < 1 or oy > 5:
            cur.close()
            return_db_connection(conn)
            return jsonify({
                "hataKodu": "BAD_REQUEST",
                "mesaj": "Oy değeri 1 ile 5 arasında olmalıdır."
            }), 400
        
        user_id = decoded['user_id']
        
        # Oy kaydet (eğer daha önce oy vermişse güncelle)
        cur.execute("""
            INSERT INTO mentor_oylari (mentor_id, kullanici_id, oy)
            VALUES (%s, %s, %s)
            ON CONFLICT (mentor_id, kullanici_id) 
            DO UPDATE SET oy = EXCLUDED.oy, olusturma_tarihi = CURRENT_TIMESTAMP
        """, (mentor_id, user_id, int(oy)))
        
        # Yeni ortalamayı hesapla
        cur.execute("""
            SELECT AVG(oy) as ortalama, COUNT(*) as toplam
            FROM mentor_oylari
            WHERE mentor_id = %s
        """, (mentor_id,))
        oy_istatistik = cur.fetchone()
        
        conn.commit()
        cur.close()
        return_db_connection(conn)
        
        yeni_ortalama = float(oy_istatistik['ortalama']) if oy_istatistik['ortalama'] else 0
        toplam_oy = oy_istatistik['toplam'] if oy_istatistik['toplam'] else 0
        
        return jsonify({
            "durum": "basarili",
            "mesaj": "Oy başarıyla kaydedildi.",
            "mentorId": mentor_id,
            "verilenOy": int(oy),
            "toplamOy": toplam_oy,
            "yeniOrtalama": round(yeni_ortalama, 1)
        }), 200
    except Exception as e:
        if conn:
            conn.rollback()
            return_db_connection(conn)
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
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # E-posta kontrolü
        cur.execute("SELECT kullanici_id FROM kullanicilar WHERE eposta = %s", (eposta,))
        if cur.fetchone():
            cur.close()
            return_db_connection(conn)
            return jsonify({
                "hataKodu": "CONFLICT",
                "mesaj": "Bu e-posta adresi zaten kayıtlı."
            }), 409
        
        # Yeni kullanıcı ekle
        cur.execute("""
            INSERT INTO kullanicilar (eposta, sifre, rol, ad_soyad)
            VALUES (%s, %s, 'kullanici', %s)
            RETURNING kullanici_id
        """, (eposta, sifre, ad_soyad))
        
        yeni_kullanici = cur.fetchone()
        conn.commit()
        cur.close()
        return_db_connection(conn)
        
        return jsonify({
            "durum": "basarili",
            "mesaj": "Kullanıcı başarıyla kaydedildi.",
            "kullaniciId": yeni_kullanici['kullanici_id']
        }), 201
    except Exception as e:
        if conn:
            conn.rollback()
            return_db_connection(conn)
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

@app.route('/istatistikler', methods=['GET'])
def istatistikler():
    """Genel platform istatistikleri"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": "Veritabanı bağlantısı kurulamadı."}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Toplam mentor sayısı
        cur.execute("SELECT COUNT(*) as toplam FROM mentorlar")
        toplam_mentor = cur.fetchone()['toplam']
        
        # Toplam kullanıcı sayısı
        cur.execute("SELECT COUNT(*) as toplam FROM kullanicilar")
        toplam_kullanici = cur.fetchone()['toplam']
        
        # Toplam danışma sayısı
        cur.execute("SELECT COUNT(*) as toplam FROM danismalar")
        toplam_danisma = cur.fetchone()['toplam']
        
        # Bekleyen danışma sayısı
        cur.execute("SELECT COUNT(*) as toplam FROM danismalar WHERE durum = 'beklemede'")
        bekleyen_danisma = cur.fetchone()['toplam']
        
        # En popüler mentor (en çok oy alan)
        cur.execute("""
            SELECT m.ad_soyad, COUNT(mo.oy_id) as oy_sayisi
            FROM mentorlar m
            LEFT JOIN mentor_oylari mo ON m.mentor_id = mo.mentor_id
            GROUP BY m.mentor_id, m.ad_soyad
            ORDER BY oy_sayisi DESC
            LIMIT 1
        """)
        en_populer = cur.fetchone()
        en_populer_mentor = en_populer['ad_soyad'] if en_populer and en_populer['oy_sayisi'] > 0 else None
        
        cur.close()
        return_db_connection(conn)
        
        return jsonify({
            "toplamMentor": toplam_mentor,
            "toplamKullanici": toplam_kullanici,
            "toplamDanisma": toplam_danisma,
            "bekleyenDanisma": bekleyen_danisma,
            "enPopulerMentor": en_populer_mentor
        }), 200
    except Exception as e:
        return_db_connection(conn)
        return jsonify({"hataKodu": "DATABASE_ERROR", "mesaj": str(e)}), 500

# ---------------- Public API Endpoint'leri ----------------

@app.route('/api/public/joke', methods=['GET'])
def get_public_joke():
    """Rastgele bir şaka getirir (Public API)"""
    try:
        response = requests.get('https://official-joke-api.appspot.com/random_joke', timeout=5)
        response.raise_for_status()
        joke_data = response.json()
        return jsonify({
            "durum": "basarili",
            "setup": joke_data.get('setup', ''),
            "punchline": joke_data.get('punchline', ''),
            "kaynak": "official-joke-api.appspot.com"
        }), 200
    except requests.exceptions.RequestException as e:
        return jsonify({
            "hataKodu": "API_ERROR",
            "mesaj": f"Şaka API'sine erişilemedi: {str(e)}"
        }), 500

@app.route('/api/public/quote', methods=['GET'])
def get_public_quote():
    """Rastgele bir alıntı getirir (Public API)"""
    try:
        response = requests.get('https://api.quotable.io/random', timeout=5)
        response.raise_for_status()
        quote_data = response.json()
        return jsonify({
            "durum": "basarili",
            "content": quote_data.get('content', ''),
            "author": quote_data.get('author', 'Bilinmeyen'),
            "tags": quote_data.get('tags', []),
            "kaynak": "api.quotable.io"
        }), 200
    except requests.exceptions.RequestException as e:
        return jsonify({
            "hataKodu": "API_ERROR",
            "mesaj": f"Alıntı API'sine erişilemedi: {str(e)}"
        }), 500

@app.route('/api/public/cat-fact', methods=['GET'])
def get_public_cat_fact():
    """Rastgele bir kedi bilgisi getirir (Public API)"""
    try:
        response = requests.get('https://catfact.ninja/fact', timeout=5)
        response.raise_for_status()
        fact_data = response.json()
        return jsonify({
            "durum": "basarili",
            "fact": fact_data.get('fact', ''),
            "length": fact_data.get('length', 0),
            "kaynak": "catfact.ninja"
        }), 200
    except requests.exceptions.RequestException as e:
        return jsonify({
            "hataKodu": "API_ERROR",
            "mesaj": f"Kedi bilgisi API'sine erişilemedi: {str(e)}"
        }), 500

@app.route('/api/public/weather', methods=['GET'])
def get_public_weather():
    """Belirtilen şehrin hava durumunu getirir (Public API)"""
    city = request.args.get('city', 'Istanbul')
    
    try:
        url = f'https://wttr.in/{city}?format=j1'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        weather_data = response.json()
        
        current = weather_data.get('current_condition', [{}])[0]
        location = weather_data.get('nearest_area', [{}])[0]
        
        return jsonify({
            "durum": "basarili",
            "sehir": city,
            "sicaklik": current.get('temp_C', 'N/A'),
            "durum": current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
            "nem": current.get('humidity', 'N/A'),
            "ruzgar": current.get('windspeedKmph', 'N/A'),
            "kaynak": "wttr.in"
        }), 200
    except requests.exceptions.RequestException as e:
        return jsonify({
            "hataKodu": "API_ERROR",
            "mesaj": f"Hava durumu API'sine erişilemedi: {str(e)}"
        }), 500

@app.route('/api/public/countries', methods=['GET'])
def get_public_countries():
    """Ülke listesini getirir (Public API)"""
    try:
        response = requests.get('https://restcountries.com/v3.1/all', timeout=10)
        response.raise_for_status()
        countries_data = response.json()
        
        # Sadece temel bilgileri döndür
        countries_list = []
        for country in countries_data[:50]:  # İlk 50 ülke
            countries_list.append({
                "name": country.get('name', {}).get('common', 'Bilinmeyen'),
                "capital": country.get('capital', ['N/A'])[0] if country.get('capital') else 'N/A',
                "region": country.get('region', 'N/A'),
                "population": country.get('population', 0)
            })
        
        return jsonify({
            "durum": "basarili",
            "toplam": len(countries_data),
            "gosterilen": len(countries_list),
            "ulkeler": countries_list,
            "kaynak": "restcountries.com"
        }), 200
    except requests.exceptions.RequestException as e:
        return jsonify({
            "hataKodu": "API_ERROR",
            "mesaj": f"Ülke API'sine erişilemedi: {str(e)}"
        }), 500

@app.route('/swagger.yaml', methods=['GET'])
def get_swagger():
    """Swagger/OpenAPI dokümantasyonunu döndürür"""
    try:
        return send_file('swagger.yaml', mimetype='text/yaml')
    except Exception as e:
        return jsonify({
            "hataKodu": "FILE_ERROR",
            "mesaj": f"Swagger dosyası bulunamadı: {str(e)}"
        }), 404

@app.route('/api/docs', methods=['GET'])
def api_docs():
    """Swagger UI için HTML sayfası"""
    swagger_html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bir Bilene Danış - API Dokümantasyonu</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui.css" />
        <style>
            body { margin: 0; padding: 0; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                window.ui = SwaggerUIBundle({
                    url: "/swagger.yaml",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout"
                });
            };
        </script>
    </body>
    </html>
    """
    return swagger_html, 200, {'Content-Type': 'text/html; charset=utf-8'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
