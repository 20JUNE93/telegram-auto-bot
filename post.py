import os
import requests
from groq import Groq
from datetime import datetime
import random
import io

# Настройки из секретов GitHub
GROQ_KEY = os.getenv('GROQ_KEY')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

# Создаём клиента Groq
client = Groq(api_key=GROQ_KEY)

# Темы для статей
TOPICS = [
    "искусственный интеллект",
    "космос и астрономия",
    "здоровье и медицина",
    "новые технологии",
    "психология",
    "наука и открытия",
    "экология",
    "программирование",
    "саморазвитие",
    "интересные факты"
]

def generate_article():
    """Генерируем статью с помощью Groq"""
    topic = random.choice(TOPICS)
    current_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    prompt = f"""Напиши интересную статью на тему: {topic}

Требования:
- Объем: 300-500 слов
- Начни с цепляющего заголовка с эмодзи
- Используй эмодзи для структуры
- Пиши простым языком
- Добавь интересные факты
- В конце сделай вывод
"""
    
    print("🤖 Генерирую статью...")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Ты - опытный писатель Telegram канала. Пиши коротко и интересно!"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=1500
    )
    
    article = response.choices[0].message.content
    print("✅ Статья сгенерирована!")
    return article

def generate_image_prompt(article):
    """Создаём промпт для изображения на основе статьи"""
    print("🎨 Генерирую промпт для изображения...")
    
    prompt = f"""На основе этого текста создай короткий промпт (1-2 строки на английском) для генерации изображения.
Промпт должен быть визуальным, ярким и захватывающим.

Текст:
{article[:300]}

Ответь ТОЛЬКО самим промптом на английском, без объяснений."""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    image_prompt = response.choices[0].message.content.strip()
    print(f"✅ Промпт: {image_prompt}")
    return image_prompt

def generate_image(image_prompt):
    """Генерируем изображение через Pollinations API"""
    print("🖼️ Генерирую изображение...")
    
    # Pollinations API (бесплатный, не требует ключа!)
    url = "https://image.pollinations.ai/prompt/" + image_prompt.replace(" ", "%20")
    
    try:
        response = requests.get(url, timeout=60)
        
        if response.status_code == 200:
            print("✅ Изображение сгенерировано!")
            return response.content  # Возвращаем бинарные данные изображения
        else:
            print(f"⚠️ Ошибка генерации: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"⚠️ Ошибка загрузки изображения: {e}")
        return None

def send_to_telegram(text, image_data=None):
    """Отправляем изображение + текст в Telegram канал"""
    
    if image_data:
        # Шаг 1: Отправляем фото с коротким заголовком
        print("📤 Отправляю фото в Telegram...")
        
        # Берём только первую строку (заголовок) для фото
        lines = text.split('\n')
        caption = lines[0][:200]  # Заголовок до 200 символов
        
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendPhoto"
        
        files = {
            'photo': ('image.jpg', image_data, 'image/jpeg')
        }
        data = {
            'chat_id': TG_CHAT_ID,
            'caption': caption,
            'parse_mode': 'HTML'
        }
        
        response1 = requests.post(url, files=files, data=data)
        result1 = response1.json()
        
        if not result1.get('ok'):
            print(f"❌ Ошибка отправки фото: {result1.get('description')}")
            return False
        
        print("✅ Фото отправлено!")
        
        # Шаг 2: Отправляем полный текст отдельным сообщением
        print("📤 Отправляю полный текст в Telegram...")
        
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        
        data = {
            'chat_id': TG_CHAT_ID,
            'text': text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        response2 = requests.post(url, data=data)
        result2 = response2.json()
        
        if result2.get('ok'):
            print("✅ Текст отправлен!")
            return True
        else:
            print(f"❌ Ошибка отправки текста: {result2.get('description')}")
            return False
    else:
        # Если нет изображения - отправляем только текст
        print("📤 Отправляю статью в Telegram...")
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        
        data = {
            'chat_id': TG_CHAT_ID,
            'text': text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        response = requests.post(url, data=data)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Успешно опубликовано!")
            return True
        else:
            print(f"❌ Ошибка: {result.get('description')}")
            return False
