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
- Объем: 400-600 слов
- Начни с цепляющего заголовка с эмодзи
- Используй эмодзи для структуры (📌 для списков, ✨ для выделения)
- Пиши простым языком
- Добавь интересные факты
- В конце сделай вывод

Формат:
🔥 [ЗАГОЛОВОК]

[Текст статьи]

Время публикации: {current_time}
"""
    
    print("🤖 Генерирую статью...")
    
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",  # Быстрая и бесплатная модель
        messages=[
            {"role": "system", "content": "Ты - профессиональный копирайтер, пишущий интересные статьи для Telegram канала."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=2000
    )
    
    article = response.choices[0].message.content
    print("✅ Статья сгенерирована!")
    return article

def send_to_telegram(text):
    """Отправляем статью в Telegram канал"""
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    
    data = {
        "chat_id": TG_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    print("📤 Отправляю в Telegram...")
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print("✅ Успешно опубликовано!")
        return True
    else:
        print(f"❌ Ошибка: {response.text}")
        return False

# Основная программа
if __name__ == "__main__":
    try:
        print("🚀 Запуск бота...")
        
        # Генерируем статью
        article = generate_article()
        
        # Отправляем в Telegram
        send_to_telegram(article)
        
        print("🎉 Готово!")
        
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        raise
