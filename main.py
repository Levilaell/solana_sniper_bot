import asyncio
import logging
from logger_setup import setup_logger
from tg_listener import start_telegram_listener
from config_manager import config # Importa a config já carregada

def main():
    # Configura o logger primeiro
    # Você pode definir o nível de log e o arquivo de log aqui ou ler da config se desejar
    log_level_str = config.get("logging", {}).get("level", "INFO").upper()
    log_file = config.get("logging", {}).get("file", "bot.log")
    
    # Mapear string de nível para valor numérico de logging
    numeric_level = getattr(logging, log_level_str, logging.INFO)
    
    logger = setup_logger(log_level=numeric_level, log_file=log_file)

    if config is None:
        logger.critical("Configuração principal não pôde ser carregada. Verifique 'config.json'. O bot não pode iniciar.")
        return

    logger.info("Iniciando o Bot de Monitoramento e Compra de Tokens Solana...")

    try:
        asyncio.run(start_telegram_listener())
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário (KeyboardInterrupt).")
    except Exception as e:
        logger.critical("Erro crítico não tratado no loop principal: %s", e, exc_info=True)
    finally:
        logger.info("Bot finalizado.")

if __name__ == '__main__':
    main()