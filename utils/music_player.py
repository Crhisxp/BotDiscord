import discord
import wavelink
from typing import Optional

class MusicQueue:
    """Clase para manejar la cola de música"""
    
    def __init__(self, max_size: int = 100):
        self.queue: list[wavelink.Playable] = []
        self.max_size = max_size
        self.history: list[wavelink.Playable] = []
    
    def add(self, track: wavelink.Playable) -> bool:
        """Añadir canción a la cola"""
        if len(self.queue) >= self.max_size:
            return False
        self.queue.append(track)
        return True
    
    def get_next(self) -> Optional[wavelink.Playable]:
        """Obtener siguiente canción"""
        if self.queue:
            track = self.queue.pop(0)
            self.history.append(track)
            return track
        return None
    
    def clear(self):
        """Limpiar la cola"""
        self.queue.clear()
    
    def is_empty(self) -> bool:
        """Verificar si la cola está vacía"""
        return len(self.queue) == 0
    
    def size(self) -> int:
        """Obtener tamaño de la cola"""
        return len(self.queue)

def format_duration(milliseconds: int) -> str:
    """Formatear duración en ms a formato legible"""
    seconds = milliseconds // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"

