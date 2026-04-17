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
    current_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    prompt = f"""Напиши интересную статью на тему: {topic}

Требования:
- Объем: 300-500 слов
- Начни с цепляющего заголовка с эмодзи
- Используй эмодзи для структуры (📌, ✨, 🔥, 💡)
- Пиши простым языком
- Добавь 2-3 интересных факта
- В конце напиши вывод или совет
- Не используй более 3 абзацев
"""
    
    print("🤖 Генерирую статью...")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # ✅ РАБОЧАЯ МОДЕЛЬ!
        messages=[
            {"role": "system", "content": "Ты - опытный писатель Telegram канала. Пиши коротко, интересно и захватывающе!"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=1500
    )
    
    article = response.choices[0].message.content
    print("✅ Статья сгенерирована!")
    return article

def send_to_telegram(text):
    """Отправляем статью в Telegram канал"""
    url = 
