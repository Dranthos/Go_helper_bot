# GO Helper

Go helper es un pequeño bot para telegram que ayuda a los usuarios de Pokemon Go a encontrar amigos

### Prerequisitos

El bot esta hecho para la versión 3.6 de Python, deberia de funcionar en cualquier version 3.x sin problemas.
Requiere de varias dependencias para poder ejecutarse, todas se pueden encontrar en PIP, accesible desde una terminal:

```
pip install pytesseract
pip install python-telegram-bot
pip install Image
```

### Instalación

Para ejecutar el bot se requiere de un token de acceso a la API de Telegram el cual puedes conseguir contactando con [BotFather](https://telegram.me/BotFather).

Además, se necesita una version de [Tesseract](https://github.com/tesseract-ocr/) instalada y preferiblemente señalada en el PATH (si lo ejecutas desde Windows).

Si no tienes Tesseract en el PATH, necesitaras añadir la siguiente linea a user.py:
```
pytesseract.pytesseract.tesseract_cmd = r'Ruta al ejecutable de Tesseract'
```

## Librerias y dependecias

* [Python telegram ](https://github.com/python-telegram-bot/python-telegram-bot) - El wrapper utilizado
* [Tesseract](https://github.com/tesseract-ocr/) - OCR para validación de perfiles

## Autor

* **Miguel Torres** - *Trabajo inicial* - [Dranthos](https://github.com/Dranthos)

## Licencia

Este proyecto esta licenciado bajo GNU GPL - Lee [LICENSE.md](LICENSE.md) para mas detalles.

## Agradecimientos

* A todos mis amigos cercanos a los que le he dado la lata para que intentaran romper el bot
