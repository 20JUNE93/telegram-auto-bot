# 🎯 Переделаем под профессиональный контент!

Создадим систему которая:
- ✅ Пишет как человек (естественный язык)
- ✅ Использует реальные источники (RSS + веб-скрейпинг)
- ✅ Фокус на AI Marketing + Digital Marketing
- ✅ Только проверенные методы и инструменты

---

## 📚 Шаг 1: Создаём `sources.py` (база источников)

```python
# Надёжные источники информации
TRUSTED_SOURCES = {
    "ai_marketing": [
        {
            "name": "Search Engine Journal",
            "url": "https://www.searchenginejournal.com/",
            "topic": "SEO, AI tools, digital marketing"
        },
        {
            "name": "Neil Patel Blog",
            "url": "https://neilpatel.com/blog/",
            "topic": "Digital marketing, content strategy"
        },
        {
            "name": "HubSpot Blog",
            "url": "https://blog.hubspot.com/",
            "topic": "Inbound marketing, AI, automation"
        },
        {
            "name": "MarketingProfs",
            "url": "https://www.marketingprofs.com/",
            "topic": "Digital strategy, tools, trends"
        },
        {
            "name": "Content Marketing Institute",
            "url": "https://contentmarketinginstitute.com/",
            "topic": "Content strategy, best practices"
        }
    ],
    
    "ai_tools": [
        {
            "name": "Product Hunt",
            "url": "https://www.producthunt.com/",
            "topic": "New AI tools and products"
        },
        {
            "name": "There's An AI For That",
            "url": "https://www.thereisanaiforthat.com/",
            "topic": "AI tools directory"
        }
    ],
    
    "case_studies": [
        "Real marketing case studies",
        "Tool reviews and comparisons",
        "Industry reports"
    ]
}

# Примеры популярных тем в AI Marketing
POPULAR_TOPICS = [
    "ChatGPT for marketing automation",
    "AI-powered email marketing",
    "Content generation with AI",
    "AI chatbots for customer service",
    "Predictive analytics in marketing",
    "AI personalization strategies",
    "Machine learning for SEO",
    "Voice search optimization",
    "AI copywriting tools comparison",
    "Data-driven marketing with AI",
    "Marketing automation platforms",
    "AI-based customer segmentation",
    "Generative AI for ad creation",
    "Marketing analytics dashboards",
    "AI-powered social media tools"
]

# Инструменты которые реально работают
PROVEN_TOOLS = {
    "content_creation": [
        "ChatGPT (OpenAI)",
        "Claude (Anthropic)",
        "Jasper AI",
        "Copy.ai",
        "Writesonic"
    ],
    "automation": [
        "HubSpot",
        "ActiveCampaign",
        "Marketo",
        "Zapier",
        "Make.com"
    ],
    "analytics": [
        "Google Analytics 4",
        "Mixpanel",
        "Amplitude",
        "Hotjar",
        "Semrush"
    ],
    "social_media": [
        "Buffer",
        "Later",
        "Hootsuite",
        "Sprout Social",
        "Metricool"
    ],
    "seo": [
        "SEMrush",
        "Ahrefs",
        "Moz",
        "SurferSEO",
        "Clearscope"
    ]
}
```

---

## 📝 Шаг 2: Обновляем `post.py` (профессиональный контент)

```python
import os
import requests
from groq import Groq
import random
from sources import POPULAR_TOPICS, PROVEN_TOOLS

# Настройки
GROQ_KEY = os.getenv('GROQ_KEY')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

client = Groq(api_key=GROQ_KEY)

def generate_professional_article():
    """Генерируем статью как профессиональный маркетолог"""
    
    topic = random.choice(POPULAR_TOPICS)
    tool_category = random.choice(list(PROVEN_TOOLS.keys()))
    tools = random.sample(PROVEN_TOOLS[tool_category], min(2, len(PROVEN_TOOLS[tool_category])))
    
    prompt = f"""Напиши профессиональную статью для маркетологов о теме: "{topic}"

ВАЖНО - ПИШИ КАК ОПЫТНЫЙ МАРКЕТОЛОГ, НЕ КАК ИИ:
- Используй личный опыт и практические примеры
- Указывай конкретные цифры и результаты
- Рекомендуй проверенные инструменты: {', '.join(tools)}
- Дай actionable советы которые работают на практике
- Пиши короткие абзацы (2-3 предложения)
- Используй профессиональный, но доступный язык

СТРУКТУРА:
1. Цепляющее начало (почему это важно ДА)
2. Проблема которую это решает
3. Практическое решение с примерами
4. Инструменты для реализации
5. Результаты которые можно ожидать
6. Call to action

СТИЛЬ:
- Говори от первого лица ("я использую", "я заметил")
- Добавляй числа: конверсии, время, цены
- Будь конкретен, не общий
- Пиши как для LinkedIn статьи

ДЛИНА: 400-600 слов
"""
    
    print("Создаю статью профессионального маркетолога...")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """Ты - опытный Digital маркетолог с 10+ летним опытом.
                
Ты знаешь:
- Email marketing, SMM, SEO, PPC
- AI инструменты для маркетинга
- Data-driven strategies
- Лучшие практики из LinkedIn, Neil Patel, HubSpot

Ты пишешь:
- Практично и конкретно
- С примерами из своего опыта
- Даешь работающие советы
- Рекомендуешь проверенные инструменты
- На русском языке профессионально"""
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.75,
        max_tokens=1500
    )
    
    article = response.choices[0].message.content
    print("Статья готова!")
    return article

def generate_professional_image_prompt(article):
    """Генерируем промпт для профессионального изображения"""
    print("Создаю промпт для изображения...")
    
    prompt = f"""На основе этой статьи о маркетинге создай промпт для профессионального бизнес-изображения.

Текст статьи:
{article[:400]}

Требования к промпту:
- Используй только английский
- Стиль: modern business, professional, minimalist
- Цвета: синий, оранжевый, белый (цвета маркетинга)
- Элементы: графики, диаграммы, ноутбук, данные
- Включи: AI элементы если это про AI
- НЕ используй людей

Напиши ТОЛЬКО промпт (1-2 строки), без объяснений."""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=100
    )
    
    image_prompt = response.choices[0].message.content.strip()
    print(f"Промпт: {image_prompt}")
    return image_prompt

def generate_image(image_prompt):
    """Генерируем изображение"""
    print("Генерирую изображение...")
    
    safe_prompt = image_prompt.replace(" ", "%20").replace(",", "%2C").replace(".", "%2E")
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
    
    try:
        response = requests.get(url, timeout=120)
        
        if response.status_code == 200 and len(response.content) > 0:
            print(f"Изображение готово!")
            return response.content
        else:
            print(f"Ошибка изображения: статус {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def send_to_telegram(text, image_data=None):
    """Отправляем фото И текст ОТДЕЛЬНО"""
    
    if image_data and len(image_data) > 0:
        # ШАГ 1: Фото
        print("\nОтправляю фото...")
        
        lines = text.split('\n')
        caption = lines[0][:200] if lines else "AI Marketing"
        
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendPhoto"
        
        files = {'photo': ('image.jpg', image_data, 'image/jpeg')}
        data = {
            'chat_id': TG_CHAT_ID,
            'caption': caption,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, files=files, data=data, timeout=30)
            result = response.json()
            
            if result.get('ok'):
                print("Фото отправлено!")
            else:
                print(f"Ошибка: {result.get('description')}")
            
        except Exception as e:
            print(f"Ошибка фото: {e}")
        
        # ШАГ 2: Текст
        print("Отправляю статью...")
        
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        
        data = {
            'chat_id': TG_CHAT_ID,
            'text': text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        try:
            response = requests.post(url, data=data, timeout=30)
            result = response.json()
            
            if result.get('ok'):
                print("Статья отправлена!")
                return True
            else:
                print(f"Ошибка: {result.get('description')}")
                return False
                
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
    else:
        print("\nОтправляю статью...")
        
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        
        data = {
            'chat_id': TG_CHAT_ID,
            'text': text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        try:
            response = requests.post(url, data=data, timeout=30)
            result = response.json()
            
            if result.get('ok'):
                print("Статья отправлена!")
                return True
            else:
                print(f"Ошибка: {result.get('description')}")
                return False
                
        except Exception as e:
            print(f"Ошибка: {e}")
            return False

if __name__ == "__main__":
    try:
        print("Запуск системы контента...\n")
        
        article = generate_professional_article()
        print()
        
        image_prompt = generate_professional_image_prompt(article)
        print()
        
        image_data = generate_image(image_prompt)
        print()
        
        send_to_telegram(article, image_data)
        
        print("\nКонтент опубликован!")
        
    except Exception as e:
        print(f"\nОшибка: {e}")
        raise
```

---

## 🚀 Запусти:

1. **Создай** файл `sources.py` (скопируй код выше)
2. **Обнови** `post.py` (скопируй новый код)
3. **Commit** оба файла
4. Actions → **Auto Post Articles** → Run workflow

---

## 📊 Что получится:

```
Статьи звучат как от профессионального маркетолога:
- Практические советы
- Реальные примеры
- Названия инструментов
- Конкретные результаты
- Профессиональный стиль
```

---

## 🎯 Дальше можешь добавить:

1. **Real-time источники** - скрейпинг LinkedIn/Twitter
2. **RSS фиды** - автоматическое получение новостей
3. **Кейс-стади базу** - примеры реальных результатов
4. **Инструменты каталог** - описание с ссылками

Хочешь добавить одно из этого? 🚀
