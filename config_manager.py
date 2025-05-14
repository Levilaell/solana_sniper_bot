import json
import logging

logger = logging.getLogger(__name__)

def load_config(config_path="config.json"):
    """
    Carrega o arquivo de configuração JSON.
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            logger.info("Configuração carregada com sucesso de %s", config_path)
            return config
    except FileNotFoundError:
        logger.error("Arquivo de configuração %s não encontrado.", config_path)
        raise
    except json.JSONDecodeError:
        logger.error("Erro ao decodificar o JSON do arquivo de configuração %s.", config_path)
        raise
    except Exception as e:
        logger.error("Erro inesperado ao carregar a configuração %s: %s", config_path, e)
        raise

# Carrega a configuração globalmente para ser importada por outros módulos
# Isso garante que seja carregado apenas uma vez.
try:
    config = load_config()
except Exception:
    # Se o config não puder ser carregado, defina como None para que as importações não quebrem
    # mas o bot não funcionará e registrará o erro.
    config = None
    logger.critical("Falha crítica ao carregar a configuração. O bot pode não funcionar corretamente.")

if config is None:
    # Se o config não foi carregado, é provável que os valores padrão abaixo causem erros
    # mas evitam erros de importação imediata de 'config' em outros módulos.
    # Uma melhor abordagem seria fazer com que cada módulo verifique se config é None.
    TELEGRAM_CONFIG = {}
    JUPITER_CONFIG = {}
    WALLET_CONFIG = {}
    RPC_ENDPOINT = ""
else:
    TELEGRAM_CONFIG = config.get('telegram', {})
    JUPITER_CONFIG = config.get('jupiter', {})
    WALLET_CONFIG = config.get('wallet', {})
    RPC_ENDPOINT = JUPITER_CONFIG.get('rpc_endpoint', "https://api.mainnet-beta.solana.com")