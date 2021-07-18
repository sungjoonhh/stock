import telegram
from FileReader import FileRader
import requests
class Telegram :
    def auto_message(self,message):
        filereader = FileRader()
        telg_dict = filereader.read_data('C:\\Users\\user\\Documents\\telegram.txt')
        token = telg_dict['token']
        chat_id = telg_dict['chat_id']
        bot = telegram.Bot(token=token)
        chat_id = chat_id

        bot.sendMessage(chat_id=chat_id, text=message)