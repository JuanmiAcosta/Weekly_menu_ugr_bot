import private
import logging
import schedule
import threading
import time
from telegram.ext import Updater, CommandHandler

run_scheduler = True

def run_schedule():
    global run_scheduler
    while run_scheduler:
        schedule.run_pending()
        time.sleep(1)

def getMenu():
    url = 'https://scu.ugr.es/?theme=pdf'
    return url

def cmd_start(update,context):
    
    username = update.message.from_user.username
    if username is None:
        username = "usuario"
    
    msg = """\
    Hola {username}! Soy Weekly_menu_ugr_bot, te mandaré todas las semanas el menú de comedores universitarios los domingos a las 09:00 am.
    """
    chat_id = update.message.chat_id
    context = context.bot.send_message(chat_id, msg.format(username=username))

    schedule.every().sunday.at("09:00").do(cmd_manda, context=context)
    #schedule.every(10).seconds.do(lambda: cmd_manda(update, context))
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

def cmd_help(update,context):

    msg = """\
    Comandos disponibles:
    /start - Inicia el bot, todos los domingos a las 09:00 am te manda el menú
    /help - Muestra mis comandos
    /manda - Te puedo pasar el menú cuando lo desees
    /stop - Para el bot :(
    """

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, msg, parse_mode='HTML')


def cmd_manda(update,context):
    
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, getMenu())

def cmd_stop(update,context):
        
        global run_scheduler
        run_scheduler = False
    
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id, "Adiós, espero verte pronto!")

def main():

    global run_scheduler
    run_scheduler = True

    token=private.TOKEN
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    #EVENTOS QUE INICIARÁN EL BOT
    dp.add_handler(CommandHandler('start', cmd_start))
    dp.add_handler(CommandHandler('help', cmd_help))
    dp.add_handler(CommandHandler('manda', cmd_manda))
    dp.add_handler(CommandHandler('stop', cmd_stop))

    #INICIAMOS EL BOT
    updater.start_polling()
    #LISTENER
    updater.idle()


if __name__ == '__main__':
    print(f'Bot iniciado y listo para servir...')
    main()