"""
Comandos relacionados con música
"""
import discord
from discord.ext import commands
from utils.music_player import MusicPlayer
from utils.logger import logger

class Music(commands.Cog):
    """Cog para comandos de música"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.player = MusicPlayer()
    
    @commands.command(name='join', aliases=['j', 'conectar'])
    async def join(self, ctx: commands.Context):
        """Conecta el bot a tu canal de voz"""
        if not ctx.author.voice:
            await ctx.send('❌ Debes estar en un canal de voz')
            return
        
        channel = ctx.author.voice.channel
        
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        
        await ctx.send(f'✅ Conectado a **{channel.name}**')
        logger.info(f"Conectado a {channel.name} en {ctx.guild.name}")
    
    @commands.command(name='leave', aliases=['disconnect', 'dc', 'salir'])
    async def leave(self, ctx: commands.Context):
        """Desconecta el bot del canal de voz"""
        if not ctx.voice_client:
            await ctx.send('❌ No estoy conectado a ningún canal')
            return
        
        await ctx.voice_client.disconnect()
        await ctx.send('👋 Desconectado')
        logger.info(f"Desconectado de {ctx.guild.name}")
    
    @commands.command(name='play', aliases=['p', 'reproducir'])
    async def play(self, ctx: commands.Context, *, query: str):
        """
        Reproduce una canción desde YouTube
        
        Uso: !play <nombre o URL>
        """
        # Conectar si no está en un canal
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('❌ Debes estar en un canal de voz')
                return
        
        # Detener reproducción actual
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        
        # Buscar canción
        await ctx.send(f'🔍 Buscando: **{query}**')
        song_info = await self.player.search_song(query)
        
        if not song_info:
            await ctx.send('❌ No se pudo encontrar la canción')
            return
        
        # Crear fuente de audio
        source = await self.player.create_audio_source(song_info['url'])
        
        if not source:
            await ctx.send('❌ Error al procesar el audio')
            return
        
        # Reproducir
        def after_playing(error):
            if error:
                logger.error(f"Error durante reproducción: {error}")
        
        ctx.voice_client.play(source, after=after_playing)
        
        # Enviar mensaje con información
        embed = discord.Embed(
            title="🎵 Reproduciendo",
            description=f"**{song_info['title']}**",
            color=discord.Color.green()
        )
        
        if song_info['thumbnail']:
            embed.set_thumbnail(url=song_info['thumbnail'])
        
        if song_info['duration']:
            minutes = song_info['duration'] // 60
            seconds = song_info['duration'] % 60
            embed.add_field(name="Duración", value=f"{minutes}:{seconds:02d}")
        
        await ctx.send(embed=embed)
        logger.info(f"Reproduciendo: {song_info['title']}")
    
    @commands.command(name='pause', aliases=['pausa'])
    async def pause(self, ctx: commands.Context):
        """Pausa la reproducción actual"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('⏸️ Música pausada')
        else:
            await ctx.send('❌ No hay música reproduciéndose')
    
    @commands.command(name='resume', aliases=['continuar'])
    async def resume(self, ctx: commands.Context):
        """Reanuda la reproducción pausada"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('▶️ Música reanudada')
        else:
            await ctx.send('❌ La música no está pausada')
    
    @commands.command(name='stop', aliases=['detener'])
    async def stop(self, ctx: commands.Context):
        """Detiene la reproducción y limpia la cola"""
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send('⏹️ Reproducción detenida')
        else:
            await ctx.send('❌ No hay música reproduciéndose')
    
    @commands.command(name='skip', aliases=['s', 'siguiente'])
    async def skip(self, ctx: commands.Context):
        """Salta a la siguiente canción"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('⏭️ Canción saltada')
        else:
            await ctx.send('❌ No hay música reproduciéndose')
    
    @commands.command(name='volume', aliases=['vol', 'v'])
    async def volume(self, ctx: commands.Context, volume: int = None):
        """
        Ajusta el volumen (0-100)
        
        Uso: !volume <número>
        """
        if volume is None:
            await ctx.send('📢 Uso: `!volume <0-100>`')
            return
        
        if not 0 <= volume <= 100:
            await ctx.send('❌ El volumen debe estar entre 0 y 100')
            return
        
        if ctx.voice_client and ctx.voice_client.source:
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f'🔊 Volumen ajustado a **{volume}%**')
        else:
            await ctx.send('❌ No hay música reproduciéndose')

async def setup(bot: commands.Bot):
    """Carga el cog"""
    await bot.add_cog(Music(bot))
