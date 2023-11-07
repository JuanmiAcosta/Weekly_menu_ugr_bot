import private
import logging
from telegram.ext import Updater, CommandHandler

def getMenu():
    url = 'https://scu.ugr.es/?theme=pdf'
    return url

def cmd_start(update,context):
    
    username = update.message.from_user.username
    if username is None:
        username = "usuario"
    
    msg = """\
    Hola {username}! Soy Weekly_menu_ugr_bot, te mandaré todas las semanas el menú de comedores universitarios para tu comodidad.
    """

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, msg.format(username=username))

def cmd_help(update,context):

    msg = """\
    Comandos disponibles:
    /start - Inicia el bot
    /help - Muestra mis comandos
    /manda - Te puedo pasar el menú cuando lo desees
    """

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, msg, parse_mode='HTML')

def cmd_manda(update,context):
    
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, getMenu())


def main():

    token=private.TOKEN
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    #EVENTOS QUE INICIARÁN EL BOT
    dp.add_handler(CommandHandler('start', cmd_start))
    dp.add_handler(CommandHandler('help', cmd_help))
    dp.add_handler(CommandHandler('manda', cmd_manda))

    #INICIAMOS EL BOT
    updater.start_polling()
    #LISTENER
    updater.idle()


if __name__ == '__main__':
    print(f'Bot iniciado y listo para servir...')
    main()