# PLAMPH Chatbot

Este repositorio contiene un sistema modular para la gestion de planta y un bot de Telegram.

## Configuracion del token

El bot de Telegram necesita un token para funcionar. Para mantenerlo fuera del codigo fuente, configura la variable de entorno `BOT_TOKEN` antes de ejecutar el bot:

```bash
export BOT_TOKEN="<tu token aqui>"
python bot_modular.py
```

El archivo `modules/config.py` lee esta variable y la comparte con el resto de modulos.
