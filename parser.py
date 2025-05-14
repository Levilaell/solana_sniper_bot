import re
import logging

logger = logging.getLogger(__name__)

# Expressão regular para encontrar endereços Solana (Base58, tipicamente 43-44 caracteres)
# Ajustado para ser um pouco mais flexível, mas focado em strings que parecem endereços.
SOLANA_ADDRESS_REGEX = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

def extract_token_address(message_text: str) -> str | None:
    """
    Extrai o primeiro endereço de token Solana encontrado em uma string de mensagem.
    """
    if not message_text:
        return None
    
    match = re.search(SOLANA_ADDRESS_REGEX, message_text)
    if match:
        token_address = match.group(0)
        # Adicionar validação de comprimento se necessário, por exemplo, len(token_address) >= 43
        logger.info("Endereço de token Solana encontrado: %s", token_address)
        return token_address
    
    logger.debug("Nenhum endereço de token Solana encontrado na mensagem.")
    return None