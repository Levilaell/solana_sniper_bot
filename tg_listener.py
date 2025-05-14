import logging
from telethon import TelegramClient, events
from config_manager import TELEGRAM_CONFIG, config
from parser import extract_token_address
from jupiter import buy_token

logger = logging.getLogger(__name__)

async def start_telegram_listener():
    if config is None:
        logger.error("Configuração não carregada. Bot não pode iniciar.")
        return

    api_id   = TELEGRAM_CONFIG.get('api_id')
    api_hash = TELEGRAM_CONFIG.get('api_hash')
    phone    = TELEGRAM_CONFIG.get('phone')        # usamos só PHONE
    channel  = TELEGRAM_CONFIG.get('channel')

    if not api_id or not api_hash or not phone or not channel:
        logger.error("Faltam api_id, api_hash, phone ou channel em config.json.")
        return

    # Aqui forçamos uso de conta de usuário
    client = TelegramClient('user_session', int(api_id), api_hash)
    await client.start(phone=phone)
    logger.info("Cliente Telegram iniciado como usuário: %s", phone)

    @client.on(events.NewMessage(chats=channel))
    async def handler(event):
        texto = event.message.message
        logger.debug("Mensagem recebida no canal %s: %s", channel, texto)

        token = extract_token_address(texto)
        if not token:
            return

        logger.info("Token detectado: %s → iniciando swap", token)
        try:
            sig = await buy_token(token)
            if sig:
                logger.info("Swap concluído. Assinatura: %s", sig)
            else:
                logger.warning("Swap não retornou assinatura.")
        except Exception as e:
            logger.error("Erro no swap de %s: %s", token, e, exc_info=True)

    logger.info("Listener ativo. Monitorando canal: %s", channel)
    await client.run_until_disconnected()
