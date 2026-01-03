"""
MCP Server Test Scripti
Bu script, MCP server'ın tool fonksiyonlarını test eder.
"""

import asyncio
import sys
import os

# Server modülünü import et
sys.path.insert(0, os.path.dirname(__file__))
from server import call_tool


async def test_tools():
    """Tool fonksiyonlarını test eder"""
    
    print("=" * 50)
    print("MCP Server Tool Testleri")
    print("=" * 50)
    
    # Test 1: Toplama
    print("\n1. Toplama Testi:")
    print("-" * 30)
    result = await call_tool("add_numbers", {"a": 15, "b": 27})
    for content in result:
        print(content.text)
    
    # Test 2: Çarpma
    print("\n2. Çarpma Testi:")
    print("-" * 30)
    result = await call_tool("multiply_numbers", {"a": 6, "b": 8})
    for content in result:
        print(content.text)
    
    # Test 3: İstatistik
    print("\n3. İstatistik Testi:")
    print("-" * 30)
    result = await call_tool("calculate_statistics", {"numbers": [10, 20, 30, 40, 50, 60]})
    for content in result:
        print(content.text)
    
    # Test 4: Şaka (Public API)
    print("\n4. Şaka Testi (Public API):")
    print("-" * 30)
    try:
        result = await call_tool("get_random_joke", {})
        for content in result:
            print(content.text)
    except Exception as e:
        print(f"Hata: {e}")
    
    # Test 5: Alıntı (Public API)
    print("\n5. Alıntı Testi (Public API):")
    print("-" * 30)
    try:
        result = await call_tool("get_random_quote", {})
        for content in result:
            print(content.text)
    except Exception as e:
        print(f"Hata: {e}")
    
    # Test 6: Kedi Bilgisi (Public API)
    print("\n6. Kedi Bilgisi Testi (Public API):")
    print("-" * 30)
    try:
        result = await call_tool("get_cat_fact", {})
        for content in result:
            print(content.text)
    except Exception as e:
        print(f"Hata: {e}")
    
    # Test 7: Hava Durumu (Public API)
    print("\n7. Hava Durumu Testi (Public API):")
    print("-" * 30)
    try:
        result = await call_tool("get_weather", {"city": "Istanbul"})
        for content in result:
            print(content.text)
    except Exception as e:
        print(f"Hata: {e}")
    
    print("\n" + "=" * 50)
    print("Testler tamamlandı!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_tools())

