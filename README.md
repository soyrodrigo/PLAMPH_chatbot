# PLAMPH Chatbot

Este repositorio contiene un sistema modular para la gestion de planta y un bot de Telegram.

## Configuracion del token

El bot de Telegram necesita un token para funcionar. Para mantenerlo fuera del codigo fuente, configura la variable de entorno `BOT_TOKEN` antes de ejecutar el bot:

```bash
export BOT_TOKEN="8079170530:AAHXC9elAL4CqDgF8Xp5csUw2-0FCaHFcf0"
python bot_modular.py
```

El archivo `modules/config.py` lee esta variable y la comparte con el resto de modulos.
