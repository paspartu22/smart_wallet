import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.ticker import FuncFormatter

#import pandas as pd

month_array = ["Январь", "Февраль", "Март", 
               "Апрель", "Май", "Июнь", 
               "Июль", "Август", "Сентябрь", 
               "Октябрь", "Ноябрь", "Декабрь"]

month_result_categories = ['Доход', 'Траты', 'Баланс в начале месяца', 'Баланс в конце месяца']

def draw_single_report(fig, person, colomn, file_name):
    #print()
    categories = get_categories()
    with open(file_name, 'r', encoding="utf-8") as file: #encoding="utf-8"
        sum_for_categories = {}
        for line in file:
            line = line.split(";")
            if len(line) < 2:
                print("here")
            if line[2] in person:    
                try:
                    if line[3].capitalize() in sum_for_categories:
                        sum_for_categories[line[3].capitalize()] += int(line[4])
                    else:
                        sum_for_categories[line[3].capitalize()] = int(line[4])
                except:
                    print('Плохая строчка')
        cell_text = []
        sum_credit = 0
        for name in categories:
            if name in sum_for_categories:    
                print(f'{name} {sum_for_categories[name]}')
                cell_text.append([name, sum_for_categories[name]])
                if name not in  ["Зарплата", "Семейное"]:
                    sum_credit += sum_for_categories[name]
        cell_text.append(["Суммарные траты", sum_credit])
        cell_text.append(["Разница", sum_for_categories["Зарплата"]-sum_credit])
        
        table_report = fig.add_subplot(230+colomn)
        table_report.axis('off')
        #ax.axis('tight')
        title = ""
        if len(person) == 1:
            title = "Траты "+ person[0]  
        else:
            title = "Общие траты"
        
        table_report.set_title(title)
        table_report = plt.table(cellText=cell_text,
                                 colLabels=["Категория", "Сумма"],
                                 loc="center",
                                 bbox=[0,0,1,1]
                                 )
        table_report.auto_set_font_size(False)
        table_report.set_fontsize(12)
        #table_report.scale(1.5, 1.5)        
        pie_chart = fig.add_subplot(233+colomn)

        portions = []
        labels = []
        for name in categories[1:]:
            if name in sum_for_categories:
                portions.append(int(sum_for_categories[name]/sum_credit*100))
                labels.append(name)
                

        pie_chart = plt.pie(portions,
                            labels=labels,
                            autopct='%1.1f%%' 
                            )

def draw_report(file_name):
    
    fig = plt.figure("Отчет", figsize=(1920/100, 1080/100), dpi=100, facecolor='w')     
    fig.clf()
    #plt.style.use('Solarize_Light2')   
    #plt.rcParams["figure.figsize"] = [7.00, 3.50]
    #plt.rcParams["figure.autolayout"] = True
    #fig.patch.set_visible(False)

    draw_single_report(fig, ["Дарья"], 1, file_name)
    draw_single_report(fig, ["Дарья", "Андрей"], 2, file_name)
    draw_single_report(fig, ["Андрей"], 3, file_name)
    fig.savefig(f'{file_name[:-4]}.png')
    return f'{file_name[:-4]}.png'
    
def get_categories():
    with open(f"{os.path.dirname(__file__)}/categories.txt", 'r', encoding='utf-8') as file:
        categories = file.read().splitlines()
        return categories



def draw_year_report(year):
    #fig = plt.figure("Отчет", figsize=(1920/100, 1080/100), dpi=100, facecolor='w')     
    #fig.clf()        
    files = os.listdir(os.path.dirname(__file__))
    #print(files)
    with open(f'{os.path.dirname(__file__)}/{year}.csv', 'w+', encoding="utf-8") as year_report:
        year_report.write('Месяц;Баланс на начало месяца;Доход;Расход;Баланс на конец месяца\n')
        year_result = []
        for month in range(1, 13):
            if f'{year}_{str(month).zfill(2)}.csv' in files:
                month_result = {'Доход':0, 'Траты':0,'Баланс в начале месяца':0, 'Баланс в конце месяца':0}
                with open(f'{os.path.dirname(__file__)}/{year}_{str(month).zfill(2)}.csv', 'r', encoding="utf-8") as file:
                    if len(year_result) > 0:
                        month_result["Баланс в начале месяца"] = year_result[-1]['Баланс в конце месяца']
                    elif f'{year-1}.csv' in files:
                        with open (f'{year-1}.csv', 'r', encoding="utf-8") as prev_year:
                            lines = prev_year.read().split('\n')
                            month_result["Баланс в начале месяца"] = int(lines[-2].split(';')[-1])
                    else:
                        month_result['Баланс в начале месяца'] = 300000 #Баланс в начале времен
                    for line in file.readlines():
                        line = line.split(';')
                        try:
                            if line[3] == 'Зарплата':
                                month_result["Доход"] += int(line[4])
                            else:
                                month_result["Траты"] += int(line[4])
                        except Exception as exception:
                            print(exception)
                            
                    
                    month_result['Баланс в конце месяца'] = month_result["Баланс в начале месяца"] + month_result["Доход"] - month_result["Траты"]
                    year_report.write(f'{month},{year};{month_result["Баланс в начале месяца"]};{month_result["Доход"]};{month_result["Траты"]};{month_result["Баланс в конце месяца"]}\n')
                    year_result.append(month_result)
                        
                print(month)
            
def plot_yearly_report(year):
    # Чтение данных из CSV файла
    df = pd.read_csv(f'{os.path.dirname(__file__)}/{year}.csv', delimiter=';')

    # Преобразование данных в нужный формат

    df['Месяц'] = pd.to_datetime(df['Месяц'], format='%m,%Y')  # Преобразуем месяц в datetime
       
    # Создание фигуры и осей
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    ax2 = ax1.twinx()  # Вторичная ось Y
    ax1.bar(df['Месяц'] - pd.DateOffset(days=3), df['Доход'], width=5, label='Доход', color='g', align='center', alpha=0.5)

    # Столбчатый график расходов
    ax1.bar(df['Месяц'] + pd.DateOffset(days=3), df['Расход'], width=5, label='Расход', color='r', align='center', alpha=0.5)

    # График баланса на начало месяца
    #ax1.plot(df['Месяц'], df['Баланс на начало месяца'], label='Баланс на начало месяца', linestyle='--', color='b')

    # График баланса на конец месяца
    ax2.plot(df['Месяц'], df['Баланс на конец месяца'], label='Баланс на конец месяца', linestyle='--', color='b')

    # Добавление заголовка и подписей
    ax1.set_title("Годовой отчет: Доходы, Расходы и Баланс")
    ax1.set_xlabel("Месяц")
    ax2.set_ylabel("Баланс", color='b')
    ax2.tick_params(axis='y', labelcolor='b')
    
    # Создание второй оси для доходов и расходов
    ax1.set_ylabel("Сумма (Доходы/Расходы)", color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    # Устанавливаем лимиты второй оси для отображения суммы доходов и расходов
    ax1.set_ylim(0, max(df['Доход'].max(), df['Расход'].max())*1.1)  # Устанавливаем лимит по доходам и расходам
    ax2.set_ylim(0, df['Баланс на конец месяца'].max()*1.1)  # Устанавливаем лимит по доходам и расходам

    # Устанавливаем пользовательский формат чисел для осей Y
    formatter = FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' '))
    ax1.yaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter(formatter)
    
    # Устанавливаем позиции меток по оси X
    ax1.set_xticks(df['Месяц'])
    # Устанавливаем формат для оси X
    ax1.set_xticklabels(df['Месяц'].dt.strftime('%b %Y'), rotation=45)
    
    # Добавление сетки
    ax1.grid(True, linestyle='--', alpha=0.7)  # Сетка для основной оси Y
    
    
    # Показать график
    ax1.legend(loc='upper center')
    ax2.legend(loc='upper left')
    #ax1.set_xticklabels(df['Месяц'].dt.strftime('%b %Y'), rotation=45)
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    #draw_report("2024_06.csv")       
    draw_year_report(2023)    
    draw_year_report(2024)
    #plot_yearly_report(2023)
    plot_yearly_report(2024)    
    
    #plt.show()
