 <title>Bir Bilene Danış - Proje Dokümantasyonu</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Inter font for better readability */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f7fafc; /* Hafif Gri Arkaplan */
        }
        /* Custom scrollbar styling for a cleaner look */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #e2e8f0;
        }
        ::-webkit-scrollbar-thumb {
            background: #4a5568;
            border-radius: 4px;
        }
        .code-block {
            background-color: #2d3748; /* Koyu Gri/Mavi (Monokai benzeri) */
            color: #f7fafc;
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            font-family: monospace;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-4xl mx-auto bg-white p-6 md:p-10 rounded-xl shadow-2xl border border-gray-100">
        <!-- Başlık -->
        <header class="mb-10 border-b pb-4">
            <h1 class="text-4xl font-extrabold text-indigo-700 mb-2">
                Bir Bilene Danış - Mentorluk Platformu Basit Backend
            </h1>
            <p class="text-gray-600 italic">
                Bu depo, ders ödevi için geliştirilmiş basit bir Python (Flask) backend ve buna ait OpenAPI (Swagger) dokümantasyonunu içerir.
            </p>
        </header>
        <!-- Kurulum ve Çalıştırma -->
        <section class="mb-10">
            <h2 class="text-3xl font-bold text-gray-800 mb-4 border-l-4 border-indigo-500 pl-3">Kurulum ve Çalıştırma</h2>
            <ol class="list-decimal list-inside space-y-4 ml-4 text-lg text-gray-700">
                <li>
                    <span class="font-semibold">Gerekli kütüphaneleri yükleyin:</span>
                    <div class="code-block mt-2">
                        <code>pip install -r requirements.txt</code>
                    </div>
                </li>
                <li>
                    <span class="font-semibold">Uygulamayı başlatın:</span>
                    <div class="code-block mt-2">
                        <code>python app.py</code>
                    </div>
                    <p class="mt-2 text-sm text-gray-500">Uygulama varsayılan olarak <code class="text-pink-400">http://127.0.0.1:5000</code> adresinde çalışacaktır.</p>
                </li>
            </ol>
        </section>
        <!-- Docker Kullanımı -->
        <section class="mb-10">
            <h2 class="text-3xl font-bold text-gray-800 mb-4 border-l-4 border-indigo-500 pl-3">Docker Kullanımı ve Dağıtım</h2>
            <p class="text-gray-700 mb-4">Proje, <code class="bg-gray-100 p-1 rounded">Dockerfile</code> ve <code class="bg-gray-100 p-1 rounded">docker-compose.yml</code> ile konteynerize edilmeye hazırdır.</p>
            <!-- İmaj Oluşturma -->
            <div class="bg-indigo-50 p-4 rounded-lg shadow-inner mb-6">
                <h3 class="text-xl font-semibold text-indigo-800 mb-2">1. İmaj Oluşturma Komutu (Ödev Çıktısı)</h3>
                <p class="text-gray-700">Aşağıdaki komut, projenin Docker imajını yerel olarak oluşturur.</p>
                <div class="code-block mt-2">
                    <code>docker build -t bir-bilene-danis .</code>
                </div>
            </div>
            <!-- Uygulamayı Çalıştırma -->
            <div class="bg-indigo-50 p-4 rounded-lg shadow-inner">
                <h3 class="text-xl font-semibold text-indigo-800 mb-2">2. Uygulamayı Çalıştırma (Compose)</h3>
                <p class="text-gray-700">Uygulamayı bir konteyner içinde arka planda (<code class="text-pink-400">-d</code>) çalıştırmak için:</p>
                <div class="code-block mt-2">
                    <code>docker-compose up -d</code>
                </div>
                <p class="mt-2 text-sm text-gray-500">Uygulama, yerel makinenizin <code class="text-pink-400">5000</code> portundan erişilebilir olacaktır: <code class="text-pink-400">http://localhost:5000/</code></p>
            </div>
        </section>
        <!-- API Dokümantasyonu -->
        <section>
            <h2 class="text-3xl font-bold text-gray-800 mb-4 border-l-4 border-indigo-500 pl-3">API Dokümantasyonu</h2>
            <p class="text-gray-700 mb-6">
                API uç noktaları ve şemaları <code class="bg-gray-100 p-1 rounded">swagger.yaml</code> dosyasında tanımlanmıştır. 
                İnteraktif dokümantasyonu görüntülemek ve test etmek için bu dosyayı 
                <a href="https://editor.swagger.io/" target="_blank" class="text-indigo-600 hover:text-indigo-800 font-medium underline">Swagger Editor</a> 
                adresine yapıştırabilirsiniz.
            </p>
            <h3 class="text-xl font-semibold text-gray-800 mb-3 border-b pb-2">Tanımlanan Uç Noktalar</h3>
            <ul class="space-y-3">
                <li class="p-3 bg-green-50 rounded-lg border border-green-200">
                    <span class="font-bold text-green-700">GET /</span> : Sağlık Kontrolü
                </li>
                <li class="p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <span class="font-bold text-blue-700">POST /kullanici/giris</span> : Giriş yapma ve JWT alma 
                    <span class="text-sm text-gray-500 ml-2">(Örn: eposta: <code class="text-pink-600">kullanici@mail.com</code>, şifre: <code class="text-pink-600">123456</code>)</span>
                </li>
                <li class="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                    <span class="font-bold text-yellow-700">GET /mentor/ara?alan=...</span> : Mentor arama 
                    <span class="text-sm text-gray-500 ml-2">(Örn: <code class="text-pink-600">?alan=Yazılım Geliştirme</code>)</span>
                </li>
                <li class="p-3 bg-red-50 rounded-lg border border-red-200">
                    <span class="font-bold text-red-700">POST /danisma/gonder</span> : Danışma talebi gönderme 
                    <span class="text-sm text-gray-500 ml-2">(JWT gereklidir)</span>
                </li>
            </ul>
        </section>
        <!-- Footer -->
        <footer class="mt-10 pt-4 border-t text-center text-gray-400 text-sm">
            Proje Ödevi Çıktısı | Python Flask Backend & Docker
        </footer>
    </div>
</body>
</html>
