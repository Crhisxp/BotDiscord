import discord
from discord.ext import commands
import wavelink
from typing import cast
import asyncio
from config.settings import (
    LAVALINK_HOST, 
    LAVALINK_PORT, 
    LAVALINK_PASSWORD, 
    LAVALINK_SECURE,
    DEFAULT_VOLUME,
    TIMEOUT_SECONDS
)
from utils.music_player import MusicQueue, format_duration
from utils.logger import logger

class Music(commands.Cog):
    """Cog de música con Wavelink y Lavalink"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queues = {}  # Guild ID: MusicQueue
        
    async def cog_load(self):
        """Se ejecuta cuando el cog se carga"""
        try:
            # Crear nodo de Lavalink
            node: wavelink.Node = wavelink.Node(
                uri=f'{"https" if LAVALINK_SECURE else "http"}://{LAVALINK_HOST}:{LAVALINK_PORT}',
                password=LAVALINK_PASSWORD
            )
            
            # Conectar al pool
            await wavelink.Pool.connect(client=self.bot, nodes=[node])
            logger.info(f"✓ Conectado a Lavalink: {LAVALINK_HOST}:{LAVALINK_PORT}")
        except Exception as e:
            logger.error(f"✗ Error conectando a Lavalink: {e}")
    
    def get_queue(self, guild_id: int) -> MusicQueue:
        """Obtener o crear cola para un servidor"""
        if guild_id not in self.queues:
            self.queues[guild_id] = MusicQueue()
        return self.queues[guild_id]
    
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload):
        """Evento cuando Lavalink está listo"""
        logger.info(f"✓ Nodo Lavalink listo: {payload.node.identifier}")
    
    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload):
        """Evento cuando una canción empieza"""
        player: wavelink.Player = payload.player
        track: wavelink.Playable = payload.track
        
        if player.guild:
            logger.info(f"▶️ Reproduciendo: {track.title} en {player.guild.name}")
    
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload):
        """Evento cuando una canción termina"""
        player: wavelink.Player = payload.player
        
        if not player.guild:
            return
        
        queue = self.get_queue(player.guild.id)
        
        # Reproducir siguiente canción si hay en la cola
        if not queue.is_empty():
            next_track = queue.get_next()
            await player.play(next_track)
        else:
            # Desconectar después de inactividad
            await asyncio.sleep(TIMEOUT_SECONDS)
            if player and not player.playing:
                await player.disconnect()
                logger.info(f"🔌 Desconectado por inactividad en {player.guild.name}")
    
    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx: commands.Context, *, busqueda: str):
        """
        Reproduce una canción desde YouTube, Spotify, SoundCloud, etc.
        
        Uso: !play <URL o nombre de canción>
        Ejemplo: !play Hillsong United
        """
        if not ctx.author.voice:
            return await ctx.send("❌ Debes estar en un canal de voz primero.")
        
        # Conectar al canal de voz
        if not ctx.voice_client:
            try:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
                await vc.set_volume(DEFAULT_VOLUME)
            except Exception as e:
                return await ctx.send(f"❌ Error al conectar: {str(e)}")
        else:
            vc: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        
        # Mensaje de búsqueda
        search_msg = await ctx.send(f"🔎 Buscando: **{busqueda}**...")
        
        try:
            # Buscar la canción (soporta YouTube, Spotify, SoundCloud automáticamente)
            tracks: wavelink.Search = await wavelink.Playable.search(busqueda)
            
            if not tracks:
                await search_msg.edit(content="❌ No se encontraron resultados.")
                return
            
            # Tomar la primera canción
            track: wavelink.Playable = tracks[0]
            
            queue = self.get_queue(ctx.guild.id)
            
            # Si está reproduciendo, añadir a la cola
            if vc.playing:
                if queue.add(track):
                    embed = discord.Embed(
                        title="✅ Añadido a la cola",
                        description=f"**[{track.title}]({track.uri})**",
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Duración", value=format_duration(track.length))
                    embed.add_field(name="Posición en cola", value=f"#{queue.size()}")
                    if track.artwork:
                        embed.set_thumbnail(url=track.artwork)
                    await search_msg.edit(content=None, embed=embed)
                else:
                    await search_msg.edit(content="❌ La cola está llena (máximo 100 canciones).")
            else:
                # Reproducir inmediatamente
                await vc.play(track)
                embed = discord.Embed(
                    title="🎵 Reproduciendo ahora",
                    description=f"**[{track.title}]({track.uri})**",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Duración", value=format_duration(track.length))
                embed.add_field(name="Solicitado por", value=ctx.author.mention)
                if track.artwork:
                    embed.set_thumbnail(url=track.artwork)
                await search_msg.edit(content=None, embed=embed)
                
        except wavelink.LavalinkException as e:
            await search_msg.edit(content=f"❌ Error de Lavalink: {str(e)}")
        except Exception as e:
            await search_msg.edit(content=f"❌ Error inesperado: {str(e)}")
            logger.error(f"Error en comando play: {e}")
    
    @commands.command(name='pause')
    async def pause(self, ctx: commands.Context):
        """Pausa o reanuda la reproducción"""
        vc: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        
        if not vc:
            return await ctx.send("❌ No estoy en un canal de voz.")
        
        await vc.pause(not vc.paused)
        
        if vc.paused:
            await ctx.send("⏸️ Reproducción pausada.")
        else:
            await ctx.send("▶️ Reproducción reanudada.")
    
    @commands.command(name='skip', aliases=['s'])
    async def skip(self, ctx: commands.Context):
        """Salta a la siguiente canción"""
        vc: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        
        if not vc or not vc.playing:
            return await ctx.send("❌ No hay nada reproduciéndose.")
        
        queue = self.get_queue(ctx.guild.id)
        
        if queue.is_empty():
            await vc.stop()
            await ctx.send("⏭️ Canción saltada. No hay más canciones en la cola.")
        else:
            await vc.stop()  # Esto activará el evento track_end que reproduce la siguiente
            await ctx.send("⏭️ Canción saltada.")
    
    @commands.command(name='stop')
    async def stop(self, ctx: commands.Context):
        """Detiene la música y limpia la cola"""
        vc: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        
        if not vc:
            return await ctx.send("❌ No estoy en un canal de voz.")
        
        queue = self.get_queue(ctx.guild.id)
        queue.clear()
        
        await vc.stop()
        await ctx.send("⏹️ Reproducción detenida y cola limpiada.")
    
    @commands.command(name='disconnect', aliases=['dc', 'leave'])
    async def disconnect(self, ctx: commands.Context):
        """Desconecta el bot del canal de voz"""
        vc: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        
        if not vc:
            return await ctx.send("❌ No estoy en un canal de voz.")
        
        queue = self.get_queue(ctx.guild.id)
        queue.clear()
        
        await vc.disconnect()
        await ctx.send("👋 Desconectado del canal de voz.")
    
    @commands.command(name='queue', aliases=['q'])
    async def queue(self, ctx: commands.Context):
        """Muestra la cola de reproducción"""
        vc: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        
        if not vc:
            return await ctx.send("❌ No estoy en un canal de voz.")
        
        queue = self.get_queue(ctx.guild.id)
        
        embed = discord.Embed(
            title="🎵 Cola de reproducción",
            color=discord.Color.blue()
        )
        
        # Canción actual
        if vc.current:
            embed.add_field(
                name="▶️ Reproduciendo ahora",
                value=f"**[{vc.current.title}]({vc.current.uri})**\nDuración: {format_duration(vc.current.length)}",
                inline=False
            )
        
        # Próximas canciones
        if not queue.is_empty():
            queue_text = ""
            for i, track in enumerate(queue.queue[:10], 1):  # Mostrar máximo 10
                queue_text += f"`{i}.` **[{track.title}]({track.uri})** - {format_duration(track.length)}\n"
            
            embed.add_field(
                name=f"📋 Próximas ({queue.size()} canciones)",
                value=queue_text,
                inline=False
            )
            
            if queue.size() > 10:
                embed.set_footer(text=f"Y {queue.size() - 10} canciones más...")
        else:
            embed.add_field(
                name="📋 Cola vacía",
                value="No hay canciones en la cola.",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='volume', aliases=['vol'])
    async def volume(self, ctx: commands.Context, volumen: int = None):
        """
        Ajusta el volumen (0-100)
        
        Uso: !volume <0-100>
        """
        vc: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        
        if not vc:
            return await ctx.send("❌ No estoy en un canal de voz.")
        
        if volumen is None:
            return await ctx.send(f"🔊 Volumen actual: **{vc.volume}%**")
        
        if not 0 <= volumen <= 100:
            return await ctx.send("❌ El volumen debe estar entre 0 y 100.")
        
        await vc.set_volume(volumen)
        await ctx.send(f"🔊 Volumen ajustado a **{volumen}%**")
    
    @commands.command(name='nowplaying', aliases=['np'])
    async def nowplaying(self, ctx: commands.Context):
        """Muestra la canción actual"""
        vc: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        
        if not vc or not vc.current:
            return await ctx.send("❌ No hay nada reproduciéndose.")
        
        track = vc.current
        
        embed = discord.Embed(
            title="🎵 Reproduciendo ahora",
            description=f"**[{track.title}]({track.uri})**",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Duración", value=format_duration(track.length))
        embed.add_field(name="Volumen", value=f"{vc.volume}%")
        
        if track.artwork:
            embed.set_thumbnail(url=track.artwork)
        
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
