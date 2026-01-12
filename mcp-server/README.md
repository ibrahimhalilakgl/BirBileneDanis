# MCP Server - Bir Bilene Danış

Bu klasör, Model Context Protocol (MCP) uyumlu bir server içerir. MCP, AI modellerinin dış kaynaklara erişmesini ve tool fonksiyonlarını kullanmasını sağlayan bir protokoldür.

## 📋 Özellikler

- ✅ **Tool Fonksiyonları** - AI modellerinin kullanabileceği çeşitli tool'lar
- ✅ **Public API Entegrasyonu** - Harici API'lerden veri çekme
- ✅ **Matematiksel İşlemler** - Toplama, çarpma, istatistik hesaplama
- ✅ **Eğlenceli İçerikler** - Şakalar, alıntılar, kedi bilgileri
- ✅ **Hava Durumu** - Şehir bazlı hava durumu sorgulama

## 🚀 Kurulum

### Gereksinimler

- Python 3.11 veya üzeri
- pip (Python paket yöneticisi)

### Adımlar

1. **MCP server klasörüne gidin:**
```bash
cd mcp-server
```

2. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

## 🛠️ Tool Fonksiyonları

### 1. add_numbers
İki sayıyı toplar.

**Parametreler:**
- `a` (number): İlk sayı
- `b` (number): İkinci sayı

**Örnek:**
```python
add_numbers(a=5, b=3)  # Sonuç: 8
```

### 2. multiply_numbers
İki sayıyı çarpar.

**Parametreler:**
- `a` (number): İlk sayı
- `b` (number): İkinci sayı

**Örnek:**
```python
multiply_numbers(a=4, b=7)  # Sonuç: 28
```

### 3. get_random_joke
Rastgele bir şaka getirir (Public API kullanır).

**Kaynak:** https://official-joke-api.appspot.com/random_joke

**Örnek:**
```python
get_random_joke()
# Çıktı: Rastgele bir şaka
```

### 4. get_random_quote
Rastgele bir alıntı getirir (Public API kullanır).

**Kaynak:** https://api.quotable.io/random

**Örnek:**
```python
get_random_quote()
# Çıktı: Rastgele bir alıntı ve yazarı
```

### 5. get_cat_fact
Rastgele bir kedi bilgisi getirir (Public API kullanır).

**Kaynak:** https://catfact.ninja/fact

**Örnek:**
```python
get_cat_fact()
# Çıktı: Rastgele bir kedi bilgisi
```

### 6. get_weather
Belirtilen şehrin hava durumunu getirir (Public API kullanır).

**Parametreler:**
- `city` (string): Şehir adı (örn: "Istanbul", "Ankara")

**Kaynak:** https://wttr.in

**Örnek:**
```python
get_weather(city="Istanbul")
# Çıktı: İstanbul'un hava durumu bilgileri
```

### 7. calculate_statistics
Sayı listesinin istatistiklerini hesaplar.

**Parametreler:**
- `numbers` (array): İstatistikleri hesaplanacak sayı listesi

**Örnek:**
```python
calculate_statistics(numbers=[10, 20, 30, 40, 50])
# Çıktı: Toplam, ortalama, minimum, maksimum değerler
```

## 🔧 Kullanım

### MCP Server'ı Başlatma

MCP server, stdio (standard input/output) üzerinden çalışır. Bir MCP client ile kullanılmalıdır.

**Manuel test için:**
```bash
python server.py
```

### MCP Client ile Kullanım

MCP server'ı kullanmak için bir MCP client'a ihtiyacınız vardır. Örneğin:

1. **Claude Desktop** - Anthropic'in Claude Desktop uygulaması MCP desteği içerir
2. **Özel MCP Client** - Kendi client'ınızı yazabilirsiniz

### MCP Client Yapılandırması

Claude Desktop için `claude_desktop_config.json` dosyasına şunu ekleyin:

```json
{
  "mcpServers": {
    "bir-bilene-danis": {
      "command": "python",
      "args": ["/path/to/mcp-server/server.py"]
    }
  }
}
```

## 📡 Public API'ler

MCP server aşağıdaki public API'leri kullanır:

1. **Joke API** - https://official-joke-api.appspot.com/random_joke
2. **Quote API** - https://api.quotable.io/random
3. **Cat Facts API** - https://catfact.ninja/fact
4. **Weather API** - https://wttr.in

Tüm API'ler ücretsiz ve herhangi bir API key gerektirmez.

## 🧪 Test

Tool fonksiyonlarını test etmek için basit bir test scripti oluşturabilirsiniz:

```python
# test_tools.py
import asyncio
from server import call_tool

async def test():
    # Toplama testi
    result = await call_tool("add_numbers", {"a": 5, "b": 3})
    print(result)
    
    # Şaka testi
    result = await call_tool("get_random_joke", {})
    print(result)

asyncio.run(test())
```

## 📦 Bağımlılıklar

- `mcp>=0.9.0` - Model Context Protocol SDK
- `requests>=2.31.0` - HTTP istekleri için

## 🔒 Güvenlik Notları

- Public API'ler ücretsizdir ancak rate limiting olabilir
- Production ortamında timeout değerlerini ayarlayın
- Hata durumlarında uygun mesajlar döndürülür

## 📝 Notlar

- MCP server stdio üzerinden çalışır, HTTP endpoint'i yoktur
- Tool fonksiyonları async olarak çalışır
- Public API'lerden gelen veriler cache'lenmez, her çağrıda yeni veri getirilir

## 🐛 Sorun Giderme

### MCP server başlamıyorsa:
- Python versiyonunu kontrol edin: `python --version`
- Paketlerin yüklü olduğundan emin olun: `pip list`
- MCP SDK'nın doğru versiyonunu yüklediğinizden emin olun

### Public API'lerden veri gelmiyorsa:
- İnternet bağlantınızı kontrol edin
- API'lerin erişilebilir olduğundan emin olun
- Timeout değerlerini artırabilirsiniz

## 📄 Lisans

Bu proje ders ödevi amaçlı geliştirilmiştir.

---

**MCP Server | Model Context Protocol | Public API Entegrasyonu**



