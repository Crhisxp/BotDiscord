# Usa imagen base ligera de Python
FROM python:3.11-slim-bullseye

# Metadata
LABEL maintainer="tu-email@ejemplo.com"
LABEL description="Discord Music Bot con Wavelink"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (ffmpeg, opus, etc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libopus0 \
    libopus-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar solo requirements primero (para cache de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear usuario no-root por seguridad
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

# Cambiar a usuario no-root
USER botuser

# Health check (opcional pero recomendado)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import discord; print('OK')" || exit 1

# Comando de inicio
CMD ["python", "-u", "bot.py"]
