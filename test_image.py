import requests

print("🧪 Тестирование Pollinations API...\n")

# Тестовый промпт
test_prompt = "A beautiful sunset over mountains with golden light, digital art"

# Преобразуем промпт для URL
safe_prompt = test_prompt.replace(" ", "%20")

url = f"https://image.pollinations.ai/prompt/{safe_prompt}"

print(f"📍 URL: {url}\n")

try:
    print("⏳ Запрашиваю изображение...")
    response = requests.get(url, timeout=120)
    
    print(f"📊 Статус код: {response.status_code}")
    print(f"📏 Размер ответа: {len(response.content)} байт")
    
    if response.status_code == 200:
        # Сохраняем локально для проверки
        with open("test_image.jpg", "wb") as f:
            f.write(response.content)
        print("✅ Изображение успешно загружено!")
        print("💾 Сохранено в test_image.jpg")
    else:
        print(f"❌ Ошибка: {response.status_code}")
        print(f"Ответ: {response.text}")
        
except requests.exceptions.Timeout:
    print("⏱️ Таймаут - изображение слишком долго генерируется")
except Exception as e:
    print(f"❌ Ошибка: {e}")
