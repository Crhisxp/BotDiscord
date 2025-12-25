"""
Configuración centralizada del bot
"""
import os
from dataclasses import dataclass

@dataclass
class Settings:
    """Configuraciones del bot"""
    
    # Token de Discord
    DISCORD_TOKEN: str = os.getenv('DISCORD_TOKEN')
    
    # Prefijo de comandos
    COMMAND_PREFIX: str = '!'
    
    # Configuración de yt-dlp
    YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }
    
    # Configuración de FFmpeg
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn -filter:a "volume=0.5"'
    }
    
    @classmethod
    def validate(cls):
        """Valida que las configuraciones necesarias estén presentes"""
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN no está configurado en las variables de entorno")

# Instancia global de configuración
config = Settings()
