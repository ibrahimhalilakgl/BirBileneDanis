# MCP Server Kurulum ve Kullanım Rehberi

## 📋 Genel Bakış

MCP (Model Context Protocol) Server, AI modellerinin dış kaynaklara erişmesini ve tool fonksiyonlarını kullanmasını sağlayan bir servistir. Bu projede, hem basit matematiksel işlemler hem de public API'lerden veri çekme özellikleri bulunmaktadır.

## 🚀 Kurulum

### 1. Gereksinimler

- Python 3.11 veya üzeri
- pip (Python paket yöneticisi)
- İnternet bağlantısı (Public API'ler için)

### 2. Adımlar

```bash
# MCP server klasörüne gidin
cd mcp-server

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

## 🛠️ Tool Fonksiyonları

### Matematiksel İşlemler

#### 1. add_numbers
İki sayıyı toplar.

**Kullanım:**
```python
add_numbers(a=10, b=20)  # Sonuç: 30
```

#### 2. multiply_numbers
İki sayıyı çarpar.

**Kullanım:**
```python
multiply_numbers(a=5, b=6)  # Sonuç: 30
```

#### 3. calculate_statistics
Sayı listesinin istatistiklerini hesaplar (toplam, ortalama, min, max).

**Kullanım:**
```python
calculate_statistics(numbers=[10, 20, 30, 40, 50])
# Çıktı:
# Toplam: 150
# Ortalama: 30.00
# Minimum: 10
# Maksimum: 50
```

### Public API Entegrasyonları

#### 4. get_random_joke
Rastgele bir şaka getirir.

**Kaynak:** https://official-joke-api.appspot.com/random_joke

**Kullanım:**
```python
get_random_joke()
```

#### 5. get_random_quote
Rastgele bir alıntı getirir.

**Kaynak:** https://api.quotable.io/random

**Kullanım:**
```python
get_random_quote()
```

#### 6. get_cat_fact
Rastgele bir kedi bilgisi getirir.

**Kaynak:** https://catfact.ninja/fact

**Kullanım:**
```python
get_cat_fact()
```

#### 7. get_weather
Belirtilen şehrin hava durumunu getirir.

**Kaynak:** https://wttr.in

**Kullanım:**
```python
get_weather(city="Istanbul")
```

## 🔧 Kullanım Senaryoları

### Senaryo 1: MCP Client ile Kullanım

MCP server, stdio (standard input/output) üzerinden çalışır. Bir MCP client ile kullanılmalıdır.

**Claude Desktop için yapılandırma:**

1. Claude Desktop'u açın
2. Yapılandırma dosyasını düzenleyin: `claude_desktop_config.json`
3. Şu yapılandırmayı ekleyin:

```json
{
  "mcpServers": {
    "bir-bilene-danis": {
      "command": "python",
      "args": ["C:/Users/Teatl/OneDrive/Desktop/BirBileneDanis-main/mcp-server/server.py"]
    }
  }
}
```

4. Claude Desktop'u yeniden başlatın
5. Claude'a tool'ları sorabilirsiniz: "İki sayıyı topla: 15 ve 27"

### Senaryo 2: Manuel Test

Tool fonksiyonlarını manuel olarak test etmek için:

```bash
cd mcp-server
python test_server.py
```

Bu script, tüm tool fonksiyonlarını test eder ve sonuçları gösterir.

### Senaryo 3: Programatik Kullanım

Kendi Python scriptinizden MCP server'ı kullanmak için:

```python
import asyncio
from mcp_server.server import call_tool

async def main():
    # Toplama işlemi
    result = await call_tool("add_numbers", {"a": 10, "b": 20})
    print(result[0].text)
    
    # Şaka getir
    result = await call_tool("get_random_joke", {})
    print(result[0].text)

asyncio.run(main())
```

## 📡 Public API Detayları

### Kullanılan API'ler

1. **Joke API**
   - URL: https://official-joke-api.appspot.com/random_joke
   - Ücretsiz, API key gerekmez
   - Rate limit: Bilinmiyor

2. **Quote API**
   - URL: https://api.quotable.io/random
   - Ücretsiz, API key gerekmez
   - Rate limit: Dakikada 60 istek

3. **Cat Facts API**
   - URL: https://catfact.ninja/fact
   - Ücretsiz, API key gerekmez
   - Rate limit: Bilinmiyor

4. **Weather API**
   - URL: https://wttr.in
   - Ücretsiz, API key gerekmez
   - Rate limit: Bilinmiyor

## 🧪 Test

### Test Scripti Çalıştırma

```bash
cd mcp-server
python test_server.py
```

### Beklenen Çıktı

```
==================================================
MCP Server Tool Testleri
==================================================

1. Toplama Testi:
------------------------------
Toplama sonucu: 15 + 27 = 42

2. Çarpma Testi:
------------------------------
Çarpma sonucu: 6 × 8 = 48

3. İstatistik Testi:
------------------------------
İstatistikler:
Toplam: 210
Ortalama: 35.00
Minimum: 10
Maksimum: 60
Sayı Adedi: 6

...
```

## 🐛 Sorun Giderme

### Problem: MCP server başlamıyor

**Çözüm:**
- Python versiyonunu kontrol edin: `python --version` (3.11+ olmalı)
- Paketlerin yüklü olduğundan emin olun: `pip list | grep mcp`
- MCP SDK'nın doğru versiyonunu yükleyin: `pip install mcp>=0.9.0`

### Problem: Public API'lerden veri gelmiyor

**Çözüm:**
- İnternet bağlantınızı kontrol edin
- API'lerin erişilebilir olduğundan emin olun (tarayıcıda test edin)
- Timeout değerlerini artırabilirsiniz (server.py dosyasında)
- Firewall veya proxy ayarlarını kontrol edin

### Problem: Claude Desktop MCP server'ı görmüyor

**Çözüm:**
- Yapılandırma dosyasının doğru konumda olduğundan emin olun
- Python path'inin doğru olduğundan emin olun
- Claude Desktop'u tamamen kapatıp yeniden açın
- Log dosyalarını kontrol edin

## 📚 Ek Kaynaklar

- [MCP Dokümantasyonu](https://modelcontextprotocol.io/)
- [Public APIs Listesi](https://github.com/public-apis/public-apis)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## 📝 Notlar

- MCP server stdio üzerinden çalışır, HTTP endpoint'i yoktur
- Tool fonksiyonları async olarak çalışır
- Public API'lerden gelen veriler cache'lenmez
- Tüm API'ler ücretsizdir ve API key gerektirmez
- Rate limiting olabilir, bu yüzden aşırı kullanımdan kaçının

---

**MCP Server | Bir Bilene Danış Projesi**

