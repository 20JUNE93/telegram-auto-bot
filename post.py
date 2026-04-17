# 🎯 Обновляем бота: человечные посты про AI маркетинг 2026


## ✅ Обновленный `post.py` с человечным стилем:


import os
import requests
from groq import Groq
import random
from datetime import datetime

GROQ_KEY = os.getenv('GROQ_KEY')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

client = Groq(api_key=GROQ_KEY)

# Актуальные темы AI маркетинга и Digital Marketing 2026
TOPICS = [
    "Как ChatGPT изменил контент-маркетинг в 2026 году",
    "AI-персонализация рекламы: кейсы крупных брендов",
    "Генеративный AI в создании креативов: что работает",
    "Predictive Analytics: как предсказывать поведение клиентов с ИИ",
    "AI-ассистенты в email-маркетинге: автоматизация нового уровня",
    "Голосовой поиск и AI: как оптимизировать контент в 2026",
    "Deepfake технологии в видеомаркетинге: этика и эффективность",
    "AI-чатботы: от поддержки к продажам",
    "Hyper-personalization: как ИИ создает уникальный опыт для каждого",
    "Computer Vision в SMM: автоматический анализ визуального контента",
    "AI для SEO: инструменты которые заменяют специалистов",
    "Нейросети для создания UGC контента",
    "Programmatic Advertising с AI: оптимизация в реальном времени",
    "AI в Influencer Marketing: поиск и анализ блогеров",
    "Sentiment Analysis: как ИИ читает эмоции аудитории",
    "AI-generated landing pages: тесты и конверсия",
    "Voice Commerce: будущее онлайн-продаж через голосовых помощников",
    "AI для A/B тестирования: миллионы вариантов за секунды",
    "Ethical AI в маркетинге: где проходит граница",
    "Omnichannel маркетинг с AI: единый клиентский путь"
]

def generate_article():
    topic = random.choice(TOPICS)
    current_date = datetime.now().strftime('%d.%m.%Y')
    
    prompt = f"""Напиши статью для Telegram канала на тему: "{topic}"

ВАЖНО - пиши как опытный маркетолог, который делится инсайтами с коллегами:
- Используй "я", "мы", "вы" 
- Делись личным опытом и наблюдениями
- Добавь 1-2 конкретных примера или кейса
- Пиши разговорным языком, без канцелярщины
- Используй метафоры и сравнения
- Задавай риторические вопросы
- Допускаются легкая ирония и юмор

Структура:
- Цепляющий заголовок с эмодзи (не банальный!)
- Короткий хук (1-2 предложения почему это важно СЕЙЧАС)
- 2-3 ключевых пункта с примерами
- Практический вывод или совет
- Призыв к действию или вопрос читателям

Объем: 400-600 слов
Тон: дружеский, экспертный, но без занудства
Избегай: штампов, общих фраз, очевидностей

Дата для контекста: {current_date}"""
    
    print(f"Генерирую статью: {topic}")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system", 
                "content": """Ты - опытный digital-маркетолог с 10+ годами опыта, который ведет популярный Telegram канал. 
                Твой стиль: живой, экспертный, с конкретными примерами. Ты не пишешь как корпоративный блог - 
                ты делишься реальным опытом. Используешь сленг индустрии, актуальные мемы, личные истории."""
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=2000
    )
    
    article = response.choices[0].message.content
    print("Статья готова!")
    return article

def generate_image_prompt(article):
    print("Создаю промпт для изображения...")
    
    prompt = f"""На основе этой маркетинговой статьи создай промпт для изображения на английском.

Статья:
{article[:400]}

Требования к промпту:
- Современный digital/tech стиль
- Яркие цвета (неон, градиенты)
- Минималистичный дизайн
- Ассоциация с AI и технологиями
- Профессионально, но креативно

Формат: "modern digital marketing illustration, [основная идея], neon colors, minimalist, professional, 4k"

Ответь ТОЛЬКО промптом на английском, без пояснений."""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150
    )
    
    image_prompt = response.choices[0].message.content.strip().strip('"')
    print(f"Промпт: {image_prompt}")
    return image_prompt

def generate_image(image_prompt):
    print("Генерирую изображение...")
    
    safe_prompt = image_prompt.replace(" ", "%20").replace(",", "%2C").replace(".", "%2E").replace('"', '')
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1200&height=630&nologo=true"
    
    try:
        response = requests.get(url, timeout=120)
        
        if response.status_code == 200 and len(response.content) > 0:
            print(f"Изображение готово! ({len(response.content)} байт)")
            return response.content
        else:
            print(f"Ошибка: статус {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Ошибка генерации: {e}")
        return None

def send_to_telegram(text, image_data=None):
    if image_data and len(image_data) > 0:
        print("\n[1/2] Отправляю изображение...")
        
        lines = text.split('\n')
        caption = lines[0][:200] if lines else ""
        
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendPhoto"
        
        files = {'photo': ('cover.jpg', image_data, 'image/jpeg')}
        data = {
            'chat_id': TG_CHAT_ID,
            'caption': caption
        }
        
        try:
            response = requests.post(url, files=files, data=data, timeout=30)
            result = response.json()
            
            if result.get('ok'):
                print("Изображение отправлено!")
            else:
                print(f"Ошибка: {result.get('description')}")
        except Exception as e:
            print(f"Ошибка отправки фото: {e}")
        
        print("\n[2/2] Отправляю текст статьи...")
        
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TG_CHAT_ID,
            'text': text,
            'disable_web_page_preview': True
        }
        
        try:
            response = requests.post(url, data=data, timeout=30)
            result = response.json()
            
            if result.get('ok'):
                print("Текст отправлен!")
            else:
                print(f"Ошибка: {result.get('description')}")
        except Exception as e:
            print(f"Ошибка отправки текста: {e}")
    else:
        print("\nОтправляю статью...")
        
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TG_CHAT_ID,
            'text': text
        }
        
        try:
            response = requests.post(url, data=data, timeout=30)
            result = response.json()
            
            if result.get('ok'):
                print("Статья опубликована!")
            else:
                print(f"Ошибка: {result.get('description')}")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    try:
        print("="*60)
        print("AI MARKETING BOT 2026")
        print("="*60 + "\n")
        
        article = generate_article()
        print()
        
        image_prompt = generate_image_prompt(article)
        print()
        
        image_data = generate_image(image_prompt)
        print()
        
        send_to_telegram(article, image_data)
        
        print("\n" + "="*60)
        print("Публикация завершена!")
        print("="*60)
        
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        raise
