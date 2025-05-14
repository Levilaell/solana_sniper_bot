import json
import logging
from solders.keypair import Keypair # Usar solders.keypair

logger = logging.getLogger(__name__)

# Importar config do config_manager
from config_manager import WALLET_CONFIG, config

def load_keypair() -> Keypair | None:
    """
    Carrega o keypair da carteira Solana de um arquivo JSON.
    O arquivo JSON deve ser uma lista de inteiros representando a chave secreta.
    """
    if config is None:
        logger.error("Configuração não carregada. Não é possível carregar o keypair.")
        return None

    keypair_path = WALLET_CONFIG.get('keypair_path')
    if not keypair_path:
        logger.error("Caminho do keypair não definido na configuração (config['wallet']['keypair_path']).")
        return None

    try:
        with open(keypair_path, 'r') as f:
            secret = json.load(f)
        logger.info("Keypair carregado com sucesso de: %s", keypair_path)
        return Keypair.from_bytes(bytes(secret)) # Keypair.from_bytes espera bytes
    except FileNotFoundError:
        logger.error("Arquivo keypair não encontrado em: %s", keypair_path)
    except json.JSONDecodeError:
        logger.error("Erro ao decodificar o JSON do arquivo keypair: %s", keypair_path)
    except Exception as e:
        logger.error("Erro inesperado ao carregar o keypair de %s: %s", keypair_path, e)
    return None