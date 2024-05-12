from datetime import datetime
import os
import creds
import telebot
from telebot import async_telebot
import asyncio

from report import draw_report
bot = async_telebot.AsyncTeleBot(creds.telegramm_api_token)
categories = {}

async def add_line_to_csv(message):
    message_data = message.text.split()
    message_data[0] = message_data[0].capitalize()
    if (message_data[0] not in categories):
        category_list = ""
        for i in categories:
            category_list += i
            category_list += "\n"
        await bot.send_message(message.chat.id, f"Категория {message_data[0]} не найдена Текущий список категориий.\n-------\n{category_list}")
        return 0
    try:
        message_data[1] = int(message_data[1])
    except Exception as error:
        await bot.send_message(message.chat.id, f"Error. Количество не число: \n{error}")
        return 0
    
    target_file = ""
    if message.text[0] == '-':
        await bot.send_message(message.chat.id, "Сохраняю в прошлый месяц")
        if int(datetime.now().date().strftime('%m')) - 1 == 0:
            target_file = f"{os.path.dirname(__file__)}/{int(datetime.now().year) - 1}_12.csv"
        else:
            target_file = f"{os.path.dirname(__file__)}/{datetime.now().year}_{'{:02d}'.format(int(datetime.now().date().strftime('%m')) - 1)}.csv"
        message.text = message.text[1:]
    else:
        target_file = f"{os.path.dirname(__file__)}/{datetime.now().year}_{datetime.now().date().strftime('%m')}.csv"
        
    try:
        with open (target_file, 'a+', encoding="utf-8") as file:
            date = datetime.now().date().strftime("%Y-%m-%d")
            #print (date)
            time = datetime.now().time().strftime("%H:%M:%S")
            #print (time)
            name = message.from_user.first_name
            #print (name)
            if  len(message_data) > 2:
                category, amount, describtion = message.text.split(" ", 2)
            elif len(message_data) == 2:
                category, amount= message_data
                describtion = " "
            else:
                await bot.send_message(message.chat.id, "Error in parsing. Line not saved")
                return 0
            #print("save data")
            print(f"{date};{time};{name};{category};{amount};{describtion}\n")
            try:     
                file.write(f"{date};{time};{name};{category};{amount};{describtion}\n")
                await bot.send_message(message.chat.id, f"Сохранено {amount} руб в категории {category}") # в файл {file.name}")
                print(f"{date};{time};{name};{category};{amount};{describtion}\n")
                return 1
            except Exception as error:
                await bot.send_message(message.chat.id, f"Error. Line not saved: {error}")
                
            print (f"recive message from {message.from_user.id}\n")    
    except Exception as error:
        await bot.send_message(message.chat.id, f"Error. File not opened: {error}")

async def add_category(message):
    try:
        new_category = message.text.split()[1].capitalize()
        await bot.send_message(message.chat.id, f"Добавляю категорию {new_category}")
        categories.append(new_category)
        with open(f"{os.path.dirname(__file__)}/categories.txt", 'a+', encoding='utf-8') as file:
            file.write(f"\n{new_category}")
        category_list = ""
        for i in categories:
            category_list += i
            category_list += "\n"
        await bot.send_message(message.chat.id, f"Текущий список категориий.\n------\n{category_list}")
    except Exception as error:
        await bot.send_message(message.chat.id, f"Error. Line caregory not added: {error}")
        
async def output_csv(message):
    try:
        target_file = f"{os.path.dirname(__file__)}/{datetime.now().year}_{datetime.now().date().strftime('%m')}.csv"
        with open(target_file, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            output_message = ""
            start = 0
            start_line = 0
            
            if len(message.text.split()) != 1:
                if (int(message.text.split()[1]) < len(lines)):
                    start = int(message.text.split()[1]) * -1 #from the end
                else:
                    start = len(lines) * -1
                start_line = len(lines) + start
            num = start_line
            while num < len(lines):
                output_message += f"{num} : {lines[num][20:]} \n"
                num += 1
                if (num % 99 == 0):
                    await bot.send_message(message.chat.id, output_message)
                    output_message = ""

            if (output_message != ""):
                await bot.send_message(message.chat.id, output_message)
            
    except Exception as error:
        await bot.send_message(message.chat.id, f"Error. output failure: {error}")
                
async def delete_line(message):
    try:
        line_num = int(message.text.split()[1])
        target_file = f"{os.path.dirname(__file__)}/{datetime.now().year}_{datetime.now().date().strftime('%m')}.csv"
        lines = ""
        with open(target_file, 'r', encoding="utf-8") as file:
            lines = file.read().splitlines()
        await bot.send_message(message.chat.id, f"Удаляю строчку {lines[line_num]}")
            
        lines.pop(line_num)
        new_file_srt = ""
        for line in lines:
            new_file_srt += f"{line}\n"
        with open(target_file, 'w', encoding="utf-8") as file:
            file.write(new_file_srt)
        await bot.send_message(message.chat.id, f"Строчка удалена")
        
        
    except Exception as error:
        await bot.send_message(message.chat.id, f"Error. Line not deleted: {error}")
     
async def output_commands(message):
    try:
        output_message = f'''
Список команд бота

= Команды              : получить список команд

= Добавить _категорию_ : добавить в лист категорий

= Список n            : вывести n последних записей. Можно оставить пустым, выведет все

= Удалить n           : удалить строчку номер n. номер строчки можно получить командой Список

= Категория 1200 описание : добавить запись. описание не обязательно

= -Категория 1200 описание: добавить запись в предыдущий месяц. описание не обязательно

= Отчет    : заказать отчет за текущий месяц
= Отчет 1  : заказать отчет за месяц №1 текущего года
= Отчет -1 : заказать отчет за предыдущий месяц
= Отчет 5 2023 : заказать отчет за конкретную дату'''   

        await bot.send_message(message.chat.id, output_message)    
                                   
    except Exception as error:
        await bot.send_message(message.chat.id, f"Error. Help fail: {error}")

async def output_report(message):
    try :                    
        target_year = 0
        target_month = 0
        if (len(message.text.split()) == 1):
            target_year = datetime.now().year
            target_month = datetime.now().date().strftime('%m')
            
        elif (len(message.text.split()) == 3):
            target_year = message.text.split()[2]
            target_month = datetime.now().date().strftime('%m')
    
        elif (len(message.text.split()) == 2):
            if (int(message.text.split()[1]) < 0):
                target_year = int(datetime.now().year)
                target_month = int(datetime.now().date().strftime('%m')) + int(message.text.split()[1])
                if (target_month <= 0):
                    target_year -= 1
                    target_month += 12
            else:
                target_year = int(datetime.now().year)
                target_month = int(message.text.split()[1])

        target_file = f"{os.path.dirname(__file__)}/{target_year}_{str(target_month).zfill(2)}.csv"                
        draw_name = draw_report(target_file)
        await bot.send_photo(message.chat.id, photo=open(draw_name, 'rb'))    
        await bot.send_message(creds.report_chat_id, f"Отчет за {target_month} {target_year}")
        await bot.send_photo(creds.report_chat_id, photo=open(draw_name, 'rb'))    
        
    except Exception as error:
        await bot.send_message(message.chat.id, f"Error. Report fail: {error}")
        
@bot.message_handler(content_types=['group'])
async def get_text_messages123(message):
    print(message.chat.id)

@bot.message_handler(content_types=['text'])
async def get_text_messages(message):
    print (message.from_user.id)
    keyword = message.text.split()[0].capitalize()
    if (message.from_user.id not in creds.users_white_list):
        await bot.send_message(message.chat.id, "You are not authorised")
        return 0
    if (keyword == "Добавить"):
        await add_category(message)
    elif (keyword == "Список"):
        await output_csv(message)
    elif (keyword == "Удалить"):
        await delete_line(message)
    elif (keyword == "Команды"):
        await output_commands(message)
    elif (keyword == "Отчет"):
        await output_report(message)
    else:
        print("start save")
        await add_line_to_csv(message)

def get_categories():
    with open(f"{os.path.dirname(__file__)}/categories.txt", 'r', encoding='utf-8') as file:
        categories = file.read().splitlines()
        return categories

if __name__ == '__main__':
    print("start bot")  
    categories = get_categories()
    asyncio.run(bot.polling(non_stop=True, request_timeout=90))

#bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть


#with open('2023_09.csv', 'a+') as file:
#    file.write ("Date;Time;Author;Section;Amount;Description\n")



