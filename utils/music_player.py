"""
Utilidades para reproducción de música
"""
import discord
import yt_dlp
import asyncio
from typing import Optional, Dict
from utils.logger import logger
from config.settings import config

class MusicPlayer:
    """Clase para manejar la reproducción de música"""
    
    def __init__(self):
        self.ytdl = yt_dlp.YoutubeDL(config.YDL_OPTIONS)
    
    async def search_song(self, query: str) -> Optional[Dict]:
        """
        Busca una canción en YouTube
        
        Args:
            query: Término de búsqueda
            
        Returns:
            Información de la canción o None si falla
        """
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None,
                lambda: self.ytdl.extract_info(f"ytsearch:{query}", download=False)
            )
            
            if 'entries' in data:
                data = data['entries'][0]
            
            return {
                'url': data['url'],
                'title': data.get('title', 'Desconocido'),
                'duration': data.get('duration', 0),
                'thumbnail': data.get('thumbnail', ''),
            }
        except Exception as e:
            logger.error(f"Error buscando canción '{query}': {e}")
            return None
    
    @staticmethod
    async def create_audio_source(url: str) -> Optional[discord.FFmpegOpusAudio]:
        """
        Crea una fuente de audio desde una URL
        
        Args:
            url: URL del audio
            
        Returns:
            Fuente de audio o None si falla
        """
        try:
            return await discord.FFmpegOpusAudio.from_probe(
                url,
                **config.FFMPEG_OPTIONS
            )
        except Exception as e:
            logger.error(f"Error creando fuente de audio: {e}")
            return None
