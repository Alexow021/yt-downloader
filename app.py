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
    update.message.reply_text("""/start restart bot from begin \n/YouTube for download YT videos as MP3 file\nany issues contact with me : @m0ha21ad""")



def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id ,text="Enjoy Ur Music :)")
    return ConversationHandler.END





def ask_for_link(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id ,text="Please Paste the video link here and wait for download... :)")
    return DOWNLOADER

def Downloader(update,context):
    try:
        link=str(update.message.text)

        Video_Url = YouTube(link)
        Video = Video_Url.streams.filter(file_extension='mp4' , only_audio= True).get_audio_only()
        vd = Video.download()

        context.bot.send_message(chat_id=update.effective_chat.id , text = f"'{Video.title}' has Downloaded successfully!")
        #context.bot.send_video(chat_id=update.effective_chat.id , video = open(vd , 'rb') , )
        context.bot.send_audio(chat_id=update.effective_chat.id , audio = open(vd , 'rb'))

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

