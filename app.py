from flask import Flask, jsonify, request
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sifrekoymaklaugrasmakistememek' 

#In-Memory Veri Yapıları
KULLANICILAR = {
    "mentor@mail.com": {"id": 101, "sifre": "123456", "rol": "mentor"},
    "kullanici@mail.com": {"id": 102, "sifre": "123456", "rol": "kullanici"}
}

MENTORLAR = [
    {"mentorId": 45, "adSoyad": "Ayşe Demir", "uzmanlikAlani": "Yazılım Geliştirme", "derecelendirme": 4.8},
    {"mentorId": 46, "adSoyad": "Burak Kaya", "uzmanlikAlani": "Kariyer Planlama", "derecelendirme": 4.5},
    {"mentorId": 47, "adSoyad": "Cem Yılmaz", "uzmanlikAlani": "Yazılım Geliştirme", "derecelendirme": 4.9}
]

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

    if not alan:
        return jsonify({"hataKodu": "BAD_REQUEST", "mesaj": "Alan parametresi gereklidir."}), 400

    eslesen_mentorlar = [m for m in MENTORLAR if alan.lower() in m['uzmanlikAlani'].lower()]

    if not eslesen_mentorlar:
        return jsonify({"hataKodu": "NOT_FOUND", "mesaj": f"'{alan}' alanında mentor bulunamadı."}), 404

    return jsonify(eslesen_mentorlar), 200

@app.route('/danisma/gonder', methods=['POST'])
def danisma_gonder():
    """Danışma Sorusu Gönderimi (Token doğrulama simülasyonu)"""
    # JWT doğrulama simülasyonu
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"hataKodu": "UNAUTHORIZED", "mesaj": "Yetkilendirme tokeni eksik."}), 403

    try:
        token = auth_header.split(' ')[1]
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({"hataKodu": "FORBIDDEN", "mesaj": "Token süresi dolmuş."}), 403
    except jwt.InvalidTokenError:
        return jsonify({"hataKodu": "FORBIDDEN", "mesaj": "Geçersiz yetkilendirme tokeni."}), 403

    #Yetkilendirme başarılı, danışma işlemini simüle et
    data = request.get_json()
    mentor_id = data.get('mentorId')

    #Mentor var mı kontrolü
    mentor_var = any(m['mentorId'] == mentor_id for m in MENTORLAR)
    if not mentor_var:
        return jsonify({"hataKodu": "NOT_FOUND", "mesaj": f"Mentor ID: {mentor_id} bulunamadı."}), 404

    return jsonify({
        "durum": "basarili",
        "danismaId": f"DS-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
        "mesaj": "Sorunuz mentora iletilmiştir. Yanıt geldiğinde bildirim alacaksınız."
    }), 201

if __name__ == '__main__':
    app.run(debug=True)
