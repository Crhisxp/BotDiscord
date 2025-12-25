import logging
import sys
from datetime import datetime

def setup_logger():
    """Configurar el logger del bot"""
    logger = logging.getLogger('bot')
    logger.setLevel(logging.INFO)
    
    # Handler para consola
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

logger = setup_logger()

