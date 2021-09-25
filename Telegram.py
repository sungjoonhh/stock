import telegram
from FileReader import FileReader


class Telegram :
    def message_Parsing(self,now_Data):
        ticker = str(now_Data['ticker'])
        date = str(now_Data['Date'])
        close = str(int(now_Data['close']))
        bol_upper_20 = str(int(now_Data['bol_upper_20']))
        bol_middle_20 = str(int(now_Data['bol_upper_20']))
        bol_down_20 = str(int(now_Data['bol_down_20']))
        bol_upper_80 = str(int(now_Data['bol_upper_80']))
        bol_middle_80 = str(int(now_Data['bol_upper_80']))
        bol_down_80 = str(int(now_Data['bol_down_80']))
        rsi = str(round(now_Data['rsi'], 2))
        agency = str(now_Data['agency'])
        foreigner = str(now_Data['foreigner'])
        ant = str(now_Data['ant'])
        message = ''

        if float(close) <= float(bol_down_20) or float(close) >= float(bol_upper_20) or float(rsi) <= 30 or float(rsi) >= 70:
            message = ('['+ticker+'] '+date +'\n' +'1. 현재주가 : '+close+' \n'+'2. 볼린저밴드 상단(20일) : '+bol_upper_20+' \n'+'3. 볼린저밴드 하단(20일선) : '+bol_down_20 +'\n'+\
               '4. 볼린저밴드 상단(80일선) : '+bol_upper_80+' \n'+'5. 볼린저밴드 하단(80일선) : '+bol_down_80 +'\n'+'6. RSI : '+rsi +'\n'+'7. 기관 순매매 : \n'+agency+'\n'+'8. 외국인 순매매 : \n'+foreigner+'\n'+\
                '9. 개미 순매매 : \n'+ant+'\n\n')

        return message
    def america_message_Parsing(self,now_Data):
        ticker = str(now_Data['ticker'])
        date = str(now_Data['Date'])
        close = str(round(now_Data['close'],2))
        bol_upper_20 = str(round(now_Data['bol_upper_20'],2))
        bol_middle_20 = str(round(now_Data['bol_upper_20'],2))
        bol_down_20 = str(round(now_Data['bol_down_20'],2))
        bol_upper_80 = str(round(now_Data['bol_upper_80'],2))
        bol_middle_80 = str(round(now_Data['bol_upper_80'],2))
        bol_down_80 = str(round(now_Data['bol_down_80'],2))
        rsi = str(round(now_Data['rsi'], 2))
        message = ''


        if float(close) <= float(bol_down_20) or float(close) >= float(bol_upper_20) or float(rsi) <= 30 or float(rsi) >= 70:
            message =  ('['+ticker+'] '+date +'\n' +'1. 현재주가 : '+close+' \n'+'2. 볼린저밴드 상단(20일) : '+bol_upper_20+' \n'+'3. 볼린저밴드 하단(20일선) : '+bol_down_20 +'\n'+\
               '4. 볼린저밴드 상단(80일선) : '+bol_upper_80+' \n'+'5. 볼린저밴드 하단(80일선) : '+bol_down_80 +'\n'+'6. RSI : '+rsi +'\n\n')
        return message


    def auto_message(self,message):
        if message == '':
            message = '[해당 종목 없음]'
        filereader = FileReader()
        telg_dict = filereader.read_data('C:\\Users\\sungjoon\\libs\\telegram.txt')
        token = telg_dict['token']
        chat_id = telg_dict['chat_id']
        bot = telegram.Bot(token=token)
        chat_id = chat_id
        print(message)
        bot.sendMessage(chat_id=chat_id, text=message)