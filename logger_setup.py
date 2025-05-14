import logging
import sys

def setup_logger(log_level=logging.INFO, log_file="bot.log"):
    """
    Configura o logger para registrar mensagens no console e em um arquivo.
    """
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console Handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Configurar o logger ao importar este módulo, se desejado, ou chamar explicitamente
# logger = setup_logger()