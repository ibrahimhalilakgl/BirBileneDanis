"""
MCP (Model Context Protocol) Server
Bu servis, AI modellerinin kullanabileceği tool fonksiyonları sağlar.
"""

import asyncio
import json
from typing import Any, Sequence
import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# MCP Server oluştur
server = Server("bir-bilene-danis-mcp")

# Public API'ler için base URL'ler
PUBLIC_APIS = {
    "jokes": "https://official-joke-api.appspot.com/random_joke",
    "quotes": "https://api.quotable.io/random",
    "cat_facts": "https://catfact.ninja/fact",
    "dog_facts": "https://dog-api.kinduff.com/api/facts",
    "weather": "https://wttr.in/{city}?format=j1"
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Kullanılabilir tool'ları listeler"""
    return [
        Tool(
            name="add_numbers",
            description="İki sayıyı toplar",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "İlk sayı"
                    },
                    "b": {
                        "type": "number",
                        "description": "İkinci sayı"
                    }
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="multiply_numbers",
            description="İki sayıyı çarpar",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "İlk sayı"
                    },
                    "b": {
                        "type": "number",
                        "description": "İkinci sayı"
                    }
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="get_random_joke",
            description="Rastgele bir şaka getirir (public API kullanır)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_random_quote",
            description="Rastgele bir alıntı getirir (public API kullanır)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_cat_fact",
            description="Rastgele bir kedi bilgisi getirir (public API kullanır)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_weather",
            description="Belirtilen şehrin hava durumunu getirir (public API kullanır)",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Şehir adı (örn: Istanbul, Ankara)"
                    }
                },
                "required": ["city"]
            }
        ),
        Tool(
            name="calculate_statistics",
            description="Sayı listesinin istatistiklerini hesaplar (ortalama, toplam, min, max)",
            inputSchema={
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "İstatistikleri hesaplanacak sayı listesi"
                    }
                },
                "required": ["numbers"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
    """Tool fonksiyonlarını çağırır"""
    
    if name == "add_numbers":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a + b
        return [TextContent(
            type="text",
            text=f"Toplama sonucu: {a} + {b} = {result}"
        )]
    
    elif name == "multiply_numbers":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a * b
        return [TextContent(
            type="text",
            text=f"Çarpma sonucu: {a} × {b} = {result}"
        )]
    
    elif name == "get_random_joke":
        try:
            response = requests.get(PUBLIC_APIS["jokes"], timeout=5)
            response.raise_for_status()
            joke_data = response.json()
            joke_text = f"{joke_data.get('setup', '')}\n{joke_data.get('punchline', '')}"
            return [TextContent(
                type="text",
                text=f"Rastgele Şaka:\n{joke_text}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Şaka alınamadı - {str(e)}"
            )]
    
    elif name == "get_random_quote":
        try:
            response = requests.get(PUBLIC_APIS["quotes"], timeout=5)
            response.raise_for_status()
            quote_data = response.json()
            quote_text = f'"{quote_data.get("content", "")}"\n- {quote_data.get("author", "Bilinmeyen")}'
            return [TextContent(
                type="text",
                text=f"Rastgele Alıntı:\n{quote_text}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Alıntı alınamadı - {str(e)}"
            )]
    
    elif name == "get_cat_fact":
        try:
            response = requests.get(PUBLIC_APIS["cat_facts"], timeout=5)
            response.raise_for_status()
            fact_data = response.json()
            return [TextContent(
                type="text",
                text=f"Kedi Bilgisi:\n{fact_data.get('fact', 'Bilgi alınamadı')}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Kedi bilgisi alınamadı - {str(e)}"
            )]
    
    elif name == "get_weather":
        city = arguments.get("city", "")
        if not city:
            return [TextContent(
                type="text",
                text="Hata: Şehir adı belirtilmedi"
            )]
        
        try:
            url = PUBLIC_APIS["weather"].format(city=city)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            weather_data = response.json()
            
            current = weather_data.get("current_condition", [{}])[0]
            temp = current.get("temp_C", "N/A")
            desc = current.get("weatherDesc", [{}])[0].get("value", "N/A")
            
            weather_text = f"{city} Hava Durumu:\nSıcaklık: {temp}°C\nDurum: {desc}"
            return [TextContent(
                type="text",
                text=weather_text
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Hava durumu alınamadı - {str(e)}"
            )]
    
    elif name == "calculate_statistics":
        numbers = arguments.get("numbers", [])
        if not numbers:
            return [TextContent(
                type="text",
                text="Hata: Sayı listesi boş"
            )]
        
        try:
            numbers = [float(n) for n in numbers]
            total = sum(numbers)
            average = total / len(numbers)
            minimum = min(numbers)
            maximum = max(numbers)
            
            stats_text = f"""İstatistikler:
Toplam: {total}
Ortalama: {average:.2f}
Minimum: {minimum}
Maksimum: {maximum}
Sayı Adedi: {len(numbers)}"""
            
            return [TextContent(
                type="text",
                text=stats_text
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: İstatistik hesaplanamadı - {str(e)}"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Bilinmeyen tool: {name}"
        )]


async def main():
    """MCP server'ı başlatır"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())



