#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import re
from user import Usuario
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
import db

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TEAM, PHOTO, INFO, NOMBRE, FCODE, FCODEI = range(6)

CANTIDAD, EXCLUSIVE, CODIGOS = range(3)

def start(bot, update, user_data):

    existe_id = db.CheckUserId(update.message.from_user.id)

    if existe_id:
        update.message.reply_text('¡Ya estas registrado!')
        return ConversationHandler.END

    update.message.reply_text(
        'Hola! Me puedes decir tu nombre de entrenador?')
    update.message.reply_text(
        'Recuerda que siempre puedes cancelar la conversación actual con el comando /cancel')
    
    user_data['usuario'] = Usuario()

    return NOMBRE


def nombre(bot, update, user_data):
    equipos = [['Rojo', 'Azul', 'Amarillo']]

    user = update.message.text
    logger.info(user)
    existe = db.CheckUser(user)

    if existe:
        update.message.reply_text('Este nombre de usuario ya esta registrado')

        return ConversationHandler.END
    else:
        user_data['usuario'].SetName(update.message.text)
        logger.info("Nombre de entrenador de %s: %s", update.message.from_user.first_name, update.message.text)
        update.message.reply_text('Entendido, ¿Cual es tu equipo?' , 
        reply_markup=ReplyKeyboardMarkup(equipos, one_time_keyboard=True))

        return TEAM

def team(bot, update, user_data):
    user_data['usuario'].SetTeam(update.message.text)
    update.message.reply_text('Genial, ahora enviame una foto de tu perfil',
                              reply_markup=ReplyKeyboardRemove())
    
    return PHOTO


def photo(bot, update, user_data):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    verificacion = user_data['usuario'].Verify_Name('user_photo.jpg')
    if verificacion:
        logger.info("Exito")
        update.message.reply_text('¡Genial! he podido validar tu nombre de entrenador: ' + user_data['usuario'].name)
        update.message.reply_text("Ahora necesito que me pases tu codigo de amigo, puedes hacerlo de dos maneras:\n\n-Mediante el boton 'Copiar codigo de Entrenador' y enviarlo a esta conversación.\n\n-Copiando los numeros directamente, con los espacios entre cada serie de 4 numeros.")

        return FCODE
    else:
        update.message.reply_text('lo siento, no he podido encontrar el nombre. Comprueba que has introducido tu nombre correctamente y vuelve a intentarlo')
        logger.info("no se ha podido validar a %s" % user.first_name)

        return ConversationHandler.END

def FCode(bot, update, user_data):
    matchObj = re.search(r'\d{4}\s\d{4}\s\d{4}',update.message.text)
    user_text = ""
    if matchObj:
        user_text = matchObj.group()
    else:
        print("No match!!")
    update.message.reply_text('El codigo que has introducido es ' + user_text +', ahora necesito una imagen que lo corrobore (pestaña amigos -> añadir amigos)')
    user_data['usuario'].SetCode(user_text)

    return FCODEI

def FCode_Image(bot, update, user_data):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('user_code_photo.jpg')
    verificacion = user_data['usuario'].Verify_Code('user_code_photo.jpg')
    if verificacion:
        logger.info("Exito")
        update.message.reply_text('¡Genial! he podido validar tu codigo de amigo: ' + user_data['usuario'].friend_code)
        db.AddUser(user_data['usuario'].name, user_data['usuario'].team, user.id, user_data['usuario'].friend_code)
        update.message.reply_text('Tu perfil ha sido creado correctamente, ahora puedes conseguir codigos de amigo con el comando /codigos')

    else:
        update.message.reply_text('lo siento, no he podido encontrar/validar el codigo, vuelve a intentarlo')

    return ConversationHandler.END
    

def exclusive(bot, update, user_data):
    equipos = [['Rojo', 'Azul', 'Amarillo','Todos']]
    user = update.message.from_user.id
    existe = db.CheckUserId(user)

    if existe:
        update.message.reply_text('¿Quieres que los códigos de amigo sean de un equipo en especial?' , 
        reply_markup=ReplyKeyboardMarkup(equipos, one_time_keyboard=True))
    
        return CANTIDAD
        
    else:
        logger.info("Intento fallido para conseguir codigos de %s: %s", update.message.from_user.first_name, update.message.from_user.id)
        update.message.reply_text('Para conseguir codigos primero tienes que registrar el tuyo con /start')

        return ConversationHandler.END    

def cantidad(bot, update, user_data):
    equipo = update.message.text
    if equipo == "Todos":
        equipo = 0
    cantidades = [["1","5","10"]]
    user_data['peticion_equipo'] = equipo

    update.message.reply_text('¿Cuantos codigos quieres que te sirva? *(LOS CODIGOS ACTUALES SON FALSOS PARA DEBUG)*', 
        reply_markup=ReplyKeyboardMarkup(cantidades, one_time_keyboard=True))
    
    return CODIGOS

def obtener_codigos(bot, update, user_data):
    codigos = db.GrabCodes(update.message.text,user_data['peticion_equipo'])
    texto = ""
    for i in codigos:
        fila = "%s - %s - %s\n" % (i[0], i[1], i[2])
        texto += fila

    update.message.reply_text('Aqui estan tus codigos:\n `%s`' % (texto), parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def info(bot, update, user_data):
    user = update.message.from_user
    info = db.CheckUserId(user.id)

    if info == False:
        update.message.reply_text("Parece que todavia no estas registrado, usa /start para crear un perfil")
        pass
    else:    
        update.message.reply_text('Tu ID de telegram es: %s' % (info[1]))
        update.message.reply_text('Tu nombre de entrenador es: %s' % (info[0]))
        update.message.reply_text('Tu equipo es: %s' % (info[2]))
        update.message.reply_text('Tu Codigo de amigo es: %s' % (info[3]))
        update.message.reply_text('Tu estado actual es: %s' % (info[4]))

def cancel(bot, update, user_data):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Cancelando conversación',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Creamos el update con el Token de la API a Telegram
    updater = Updater("TU TOKEN AQUI")

    dp = updater.dispatcher

    #Handler para el registro
    registro_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],

        states={
            TEAM: [RegexHandler('^(Rojo|Azul|Amarillo)$', team, pass_user_data=True)],

            PHOTO: [MessageHandler(Filters.photo, photo, pass_user_data=True)],

            INFO: [MessageHandler(Filters.text, info, pass_user_data=True)],

            NOMBRE: [MessageHandler(Filters.text, nombre, pass_user_data=True)],

            FCODE: [RegexHandler('^(¡Comencemos una buena amistad en Pokémon GO! ¡Mi código de Entrenador es|\d{4})', FCode, pass_user_data=True)],

            FCODEI: [MessageHandler(Filters.photo, FCode_Image, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )
    #Handler para coger codigos de la bbdd
    codigos_handler = ConversationHandler(
        entry_points=[CommandHandler('codigos', exclusive, pass_user_data=True)],

        states={

            CANTIDAD: [RegexHandler('^(Rojo|Azul|Amarillo|Todos)$', cantidad, pass_user_data=True)],

            CODIGOS: [RegexHandler('^(1|5|10)$', obtener_codigos, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]

    )

    dp.add_handler(registro_handler)
    dp.add_handler(codigos_handler)
    dp.add_handler(CommandHandler("info", info, pass_user_data=True))

    # logger de errores
    dp.add_error_handler(error)

    # Inicia el bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()