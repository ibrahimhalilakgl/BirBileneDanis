Bir Bilene Danış - Mentorluk Platformu Basit Backend

Bu depo, ders ödevi için geliştirilmiş basit bir Python (Flask) backend ve buna ait OpenAPI (Swagger) dokümantasyonunu içerir.

Kurulum ve Çalıştırma

Gerekli kütüphaneleri yükleyin:

pip install -r requirements.txt


Uygulamayı başlatın:

python app.py


Uygulama varsayılan olarak http://127.0.0.1:5000 adresinde çalışacaktır.

Docker Kullanımı ve Dağıtım

Proje, Dockerfile ve docker-compose.yml ile konteynerize edilmeye hazırdır.

1. İmaj Oluşturma Komutu (Ödev Çıktısı)

Aşağıdaki komut, projenin Docker imajını yerel olarak oluşturur.

docker build -t bir-bilene-danis .


2. Uygulamayı Çalıştırma (Compose)

Uygulamayı bir konteyner içinde arka planda (detached mode: -d) çalıştırmak için:

docker-compose up -d


Uygulama, yerel makinenizin 5000 portundan erişilebilir olacaktır: http://localhost:5000/

API Dokümantasyonu

API uç noktaları ve şemaları swagger.yaml dosyasında tanımlanmıştır. İnteraktif dokümantasyonu görüntülemek için bu dosyayı Swagger Editor adresine yapıştırabilirsiniz.

Tanımlanan Uç Noktalar

GET / : Sağlık Kontrolü

POST /kullanici/giris : Giriş yapma ve JWT alma (Örn: eposta: kullanici@mail.com, sifre: 123456)

GET /mentor/ara?alan=... : Mentor arama (Örn: ?alan=Yazılım Geliştirme)

POST /danisma/gonder : Danışma talebi gönderme (JWT gereklidir)
