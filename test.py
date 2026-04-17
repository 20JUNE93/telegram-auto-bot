import os

print("🔍 Проверка секретов...")

GROQ_KEY = os.getenv('GROQ_KEY')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

print(f"GROQ_KEY: {'✅ есть' if GROQ_KEY else '❌ НЕТ'}")
print(f"TG_BOT_TOKEN: {'✅ есть' if TG_BOT_TOKEN else '❌ НЕТ'}")
print(f"TG_CHAT_ID: {'✅ есть' if TG_CHAT_ID else '❌ НЕТ'}")

if GROQ_KEY:
    print(f"GROQ_KEY начинается с: {GROQ_KEY[:10]}...")
if TG_BOT_TOKEN:
    print(f"TG_BOT_TOKEN начинается с: {TG_BOT_TOKEN[:10]}...")
if TG_CHAT_ID:
    print(f"TG_CHAT_ID: {TG_CHAT_ID}")
