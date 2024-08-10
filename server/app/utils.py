from .settings import settings
import aiohttp


async def send_telegram_message(message: str):
    if not (settings.BOT_TOKEN and settings.ADMIN_CHAT_ID):
        return
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': settings.ADMIN_CHAT_ID,
        'text': message
    }
    async with aiohttp.ClientSession() as client:
        response = await client.post(url, data=payload)
        if response.status != 200:
            raise Exception(f"Ошибка отправки сообщения: {response.text}")
