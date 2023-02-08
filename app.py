import telegram.ext
from telegram import *
import json
import os
from pytube import YouTube

from telegram.ext import *


TOKEN = json.load(open("token.json" , "r"))
DOWNLOADER = 0




updater = telegram.ext.Updater( TOKEN , use_context = True)
dispatcher = updater.dispatcher


def start( update , context ):
    update.message.reply_text("for get help use /help or /YouTube\nwe have api limitations")


def help( update , context ):
    update.message.reply_text("""/start restart bot from begin \n/YouTube for download YT videos and show what bot can do with that command\nany issues contact with me : @id""")



def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id ,text=""" 
            we're sorry if it's not '1080p' because it's a restriction from Telegram\nCheck telegram api limits https://core.telegram.org/bots/api#senddocument\nbut we're found solution..we will fix it soon...""")
    return ConversationHandler.END





def ask_for_link(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id ,text="Please Paste the video link here and wait for download... :) [we have api limitations]")
    return DOWNLOADER

def Downloader(update,context):
    try:
        link=str(update.message.text)

        Video_Url = YouTube(link)
        Video = Video_Url.streams.filter(file_extension='mp4').get_highest_resolution()
        vd = Video.download()

        context.bot.send_message(chat_id=update.effective_chat.id , text = f"'{Video.title}' has Downloaded successfully! [if not received video because of api limitations please wait 60sec then try again]")
        context.bot.send_video(chat_id=update.effective_chat.id , video = open(vd , 'rb'))

        stop(update , context)
        os.remove(vd)
        return YouTube_Downloader_converstation_handler.END
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id , text = "something went wrong! its a text or unsupported link")
        return YouTube_Downloader_converstation_handler.END



YouTube_Downloader_converstation_handler=ConversationHandler(
    entry_points=[CommandHandler("YouTube", ask_for_link)] , 
    states={
        DOWNLOADER :[MessageHandler(Filters.text , callback=Downloader )]
        
        },
    fallbacks=[telegram.ext.CommandHandler("quit" , quit)]) 




#adding commands to dispatcher
dispatcher.add_handler(YouTube_Downloader_converstation_handler)
dispatcher.add_handler(telegram.ext.CommandHandler('start' , start))
dispatcher.add_handler(telegram.ext.CommandHandler('help' , help))
dispatcher.add_handler(telegram.ext.CommandHandler('YouTube' , YouTube))


updater.start_polling(timeout=600)
updater.idle()

