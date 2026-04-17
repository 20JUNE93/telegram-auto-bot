import os
import requests
from groq import Groq
from datetime import datetime
import random

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
    
    # Преобразуем промпт для URL (экранируем спецсимволы)
    safe_prompt = image_prompt.replace(" ", "%20").replace(",", "%2C").replace(".", "%2E")
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
    
    try:
        print(f"⏳ Запрашиваю изображение...")
        response = requests.get(url, timeout=120)
        
        if response.status_code == 200 and len(response.content) > 0:
            print(f"✅ Изображение сгенерировано! 
