import matplotlib.pyplot as plt
import os

#import pandas as pd


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
                if line[3].capitalize() in sum_for_categories:
                    sum_for_categories[line[3].capitalize()] += int(line[4])
                else:
                    sum_for_categories[line[3].capitalize()] = int(line[4])
        
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
    
    fig = plt.figure("Отчет", figsize=(1920/100, 1080/100), dpi=100)
    
    #plt.rcParams["figure.figsize"] = [7.00, 3.50]
    #plt.rcParams["figure.autolayout"] = True
    fig.patch.set_visible(False)
    draw_single_report(fig, ["Дарья"], 1, file_name)
    draw_single_report(fig, ["Дарья", "Андрей"], 2, file_name)
    draw_single_report(fig, ["Андрей"], 3, file_name)
    fig.savefig(f'{file_name[:-4]}.png')
    return f'{file_name[:-4]}.png'
    
def get_categories():
    with open(f"{os.path.dirname(__file__)}/categories.txt", 'r', encoding='utf-8') as file:
        categories = file.read().splitlines()
        return categories
    
if __name__ == "__main__":
    draw_report("2024_04.csv")        
    plt.show()
