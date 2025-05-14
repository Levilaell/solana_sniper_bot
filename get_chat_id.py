from telethon.sync import TelegramClient
from config_manager import TELEGRAM_CONFIG

api_id   = TELEGRAM_CONFIG['api_id']
api_hash = TELEGRAM_CONFIG['api_hash']
phone    = TELEGRAM_CONFIG['phone']

with TelegramClient('tmp_session', api_id, api_hash) as client:
    # Use o link do convite do canal
    entity = client.get_entity('https://t.me/+MyW8zbN-DxE3MjRh')
    print("Chat title:", entity.title)
    print("Chat ID numérico:", entity.id)
