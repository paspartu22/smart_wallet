from datetime import datetime
import os
import creds

import telebot
from telebot import async_telebot
import asyncio

bot = async_telebot.AsyncTeleBot(creds.api_token)

async def add_line_to_csv(message):
    try:
        with open (f"{os.path.dirname(__file__)}/{datetime.now().year}_{datetime.now().date().strftime('%m')}.csv", 'a+', encoding="utf-8") as file:
            date = datetime.now().date().strftime("%Y-%m-%d")
            #print (date)
            time = datetime.now().time().strftime("%H:%M:%S")
            #print (time)
            name = message.from_user.first_name
            #print (name)
            if  len(message.text.split()) > 2:
                category, amount, describtion = message.text.split(" ", 2)
            elif len(message.text.split()) == 2:
                category, amount= message.text.split()
                describtion = " "
            else:
                await bot.send_message(message.chat.id, "Error in parsing. Line not saved")
                return 0
            #print("save data")
            print(f"{date};{time};{name};{category};{amount};{describtion}\n")
            try:     
                file.write(f"{date};{time};{name};{category};{amount};{describtion}\n")
                await bot.send_message(message.chat.id, f"Сохранено {amount}руб в категории {category}") # в файл {file.name}")
                print(f"{date};{time};{name};{category};{amount};{describtion}\n")
                return 1
            except Exception as error:
                await bot.send_message(message.chat.id, f"Error. Line not saved: {error}")
                
            print (f"recive message from {message.from_user.id}\n")    
    except Exception as error:
        await bot.send_message(message.chat.id, f"Error. File not opened: {error}")

@bot.message_handler(content_types=['text'])
async def get_text_messages(message):
    print (message.from_user.id)
    if (message.from_user.id not in creds.users_white_list):
        await bot.send_message(message.chat.id, "You are not authorised")
        return 0
    print("start save")
    await add_line_to_csv(message)


if __name__ == '__main__':
    print("start bot")  
    asyncio.run(bot.polling(non_stop=True, request_timeout=90))

#bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть


#with open('2023_09.csv', 'a+') as file:
#    file.write ("Date;Time;Author;Section;Amount;Description\n")



