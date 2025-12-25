# 🎵 Bot de Música para Discord

Bot de música profesional con soporte para YouTube, Spotify, SoundCloud usando Wavelink y Lavalink.

## ✨ Características

- ✅ Sin errores HTTP 403 de YouTube
- 🎵 Soporte para YouTube, Spotify, SoundCloud, Apple Music
- 📋 Sistema de cola avanzado
- 🔊 Control de volumen
- ⚡ Reproducción rápida y sin interrupciones
- 🎨 Embeds con información detallada

1. **Clona el repositorio**

git clone <tu-repo>
cd BOTDISCORD

2. **Instala las dependencias**
pip install -r requirements.txt

3. **Configura el archivo .env**
DISCORD_TOKEN=tu_token_aqui
LAVALINK_HOST=lavalink.jirayu.net
LAVALINK_PORT=13592
LAVALINK_PASSWORD=youshallnotpass
LAVALINK_SECURE=False
PREFIX=!

4. **Ejecuta el bot**
python bot.py

## 📝 Comandos

### Música
- `!play <canción>` - Reproduce música
- `!pause` - Pausa/reanuda
- `!skip` - Siguiente canción
- `!stop` - Detener y limpiar cola
- `!queue` - Ver cola
- `!nowplaying` - Canción actual
- `!volume <0-100>` - Ajustar volumen
- `!disconnect` - Desconectar bot

### General
- `!ping` - Latencia del bot
- `!info` - Información del bot
- `!help` - Ayuda

## 🔧 Servidores Lavalink Públicos Gratuitos

El bot usa servidores públicos de Lavalink. Opciones disponibles:

- `lavalink.jirayu.net:13592` (por defecto)
- `lavalink.devamop.in:443`
- `lava.link:80`

## 📦 Tecnologías

- discord.py 2.x
- Wavelink
- Lavalink v4
- Python 3.11+

## 📄 Licencia

MIT License
