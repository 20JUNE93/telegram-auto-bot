import os
import requests
from groq import Groq
import random

# Настройки
GROQ_KEY = os.getenv('GROQ_KEY')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

print("=" * 60)
print("🔍 ПОЛНАЯ ДИАГНОСТИКА")
print("=" * 60)

# Проверка секретов
print("\n📋 Секреты:")
print(f"  GROQ_KEY: {'✅' if GROQ_KEY else '❌'}")
print(f"  TG_BOT_TOKEN: {'✅' if TG_BOT_TOKEN else '❌'}")
print(f"  TG_CHAT_ID: {'✅' if TG_CHAT_ID else '❌'}")

if not all([GROQ_KEY, TG_BOT_TOKEN, TG_CHAT_ID]):
    print("\n❌ Не все секреты установлены!")
    exit(1)

# Шаг 1: Генерируем статью
print("\n" + "=" * 60)
print("📝 ШАГ 1: Генерация статьи")
print("=" * 60)

client = Groq(api_key=GROQ_KEY)

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Напиши короткую статью (200 слов) о космосе"}
        ],
        max_tokens=500
    )
    
    article = response.choices[0].message.content
    print(f"✅ Статья сгенерирована ({len(article)} символов)")
    print(f"\nТекст: {article[:100]}...")
    
except Exception as e:
    print(f"❌ Ошибка Groq: {e}")
    exit(1)

# Шаг 2: Генерируем промпт для изображения
print("\n" + "=" * 60)
print("🎨 ШАГ 2: Генерация промпта для изображения")
print("=" * 60)

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": f"Создай короткий промпт (1 строка на английском) для изображения на основе: {article[:200]}"}
        ],
        max_tokens=100
    )
    
    image_prompt = response.choices[0].message.content.strip()
    print(f"✅ Промпт готов: {image_prompt}")
    
except Exception as e:
    print(f"❌ Ошибка генерации промпта: {e}")
    exit(1)

# Шаг 3: Генерируем изображение
print("\n" + "=" * 60)
print("🖼️ ШАГ 3: Генерация изображения")
print("=" * 60)

try:
    safe_prompt = image_prompt.replace(" ", "%20").replace(",", "%2C")
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
    
    print(f"📍 URL: {url[:80]}...")
    
    response = requests.get(url, timeout=120)
    
    print(f"📊 Статус код: {response.status_code}")
    print(f"📏 Размер: {len(response.content)} байт")
    
    if response.status_code == 200 and len(response.content) > 0:
        image_data = response.content
        print(f"✅ Изображение загружено! Размер: {len(image_data)} байт")
    else:
        print(f"❌ Ошибка: пустой ответ!")
        image_data = None
        
except Exception as e:
    print(f"❌ Ошибка загрузки изображения: {e}")
    image_data = None

# Шаг 4: Отправляем в Telegram
print("\n" + "=" * 60)
print("📱 ШАГ 4: Отправка в Telegram")
print("=" * 60)

print(f"Chat ID: {TG_CHAT_ID}")
print(f"Есть изображение: {'✅ Да' if image_data else '❌ Нет'}")

if image_data:
    print("\n📤 Отправляю фото...")
    
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendPhoto"
    
    files = {
        'photo': ('image.jpg', image_data, 'image/jpeg')
    }
    data = {
        'chat_id': TG_CHAT_ID,
        'caption': article[:300],
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, files=files, data=data, timeout=30)
        result = response.json()
        
        print(f"📊 Статус: {response.status_code}")
        print(f"✅ ok: {result.get('ok')}")
        
        if result.get('ok'):
            print("✅ Фото успешно отправлено!")
        else:
            print(f"❌ Ошибка: {result.get('description')}")
            
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
else:
    print("\n⚠️ Изображение не загружено, отправляю только текст...")
    
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    
    data = {
        'chat_id': TG_CHAT_ID,
        'text': article,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=data, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Текст успешно отправлен!")
        else:
            print(f"❌ Ошибка: {result.get('description')}")
            
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

print("\n" + "=" * 60)
print("🎉 ТЕСТ ЗАВЕРШЕН")
print("=" * 60)
