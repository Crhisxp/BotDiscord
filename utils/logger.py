"""
Sistema de logging personalizado
"""
import logging
from datetime import datetime

def setup_logger(name: str = 'bot') -> logging.Logger:
    """
    Configura y retorna un logger personalizado
    
    Args:
        name: Nombre del logger
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Formato del log
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Logger global
logger = setup_logger()
