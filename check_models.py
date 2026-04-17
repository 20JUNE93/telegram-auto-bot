from groq import Groq
import os

GROQ_KEY = os.getenv('GROQ_KEY')
client = Groq(api_key=GROQ_KEY)

print("🔍 Доступные модели Groq:\n")

try:
    models = client.models.list()
    
    for model in models.data:
        print(f"✅ {model.id}")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
