import requests
from datetime import datetime
from os import rename,path,mkdir, renames

#Парсинг json в python
users = requests.get("https://json.medrating.org/users")
todos = requests.get("https://json.medrating.org/todos")

#Определение глобальных переменных и даты/время 
now = datetime.now()
now_file = now.strftime("%d.%m.%Y %H:%M")
now_name = now.strftime("%Y-%m-%d %H;%M")
dir_name = "tasks"
n = 1
max_id = 1

#Начало цикла формирования отчёта 
def start():
    #Проверка наличия директории и её создание
    def check():
        if path.exists(dir_name):
            pass
        else:
            mkdir("tasks")
            check()
    check()

    #Сканирование файла users и вывод данныхпо ключу 
    with open("tasks/user.txt", "w", encoding='utf=8') as file:
        for data in users.json():
            user_id = data['id']
            array = []
            array.append(user_id)
            global max_id                  #Переопределение глобальной переменной с максимальным id пользователя для запуска цикла
            max_id=max(array)
            if user_id == n:
                file.write(f"Отчёт для {data['company']['name']}.\n{data['name']} <{data['email']}> {now_file} \n")
                nickname = data['username']      #Передача username пользователя в переменную, для последующего переименования документа

    #Определние общего количества задач и внесение их в список по степени выполнения
    try:
        with open("tasks/user.txt", "r", encoding='utf=8') as file:
            count = 0
            done = 0
            done_array = []
            not_done = 0
            not_done_array = []
            for task in todos.json():
                userId = task['userId']
                completed = task['completed']
                if userId == n:
                    count+=1         
                    if completed == True:
                        done+=1
                        done_array.append(task['title'])
                    else: 
                        not_done+=1
                        not_done_array.append(task['title'])
    except KeyError:
        pass 

    #Определение, есть ли задачи у пользователя
    if count == 0:
        with open ('tasks/user.txt', "a", encoding='utf=8') as file:
            file.write(f"У пользователя нет задач\n")
    else:
        #Вывод общего количества задач
        with open ('tasks/user.txt', "a", encoding='utf=8') as file:
            file.write(f"Всего задач: {count}\n\nЗавершённые задачи ({done}):\n")

        #Вывод списка с завершёнными задачами
        with open ('tasks/user.txt', "a") as file:
            for item in done_array:
                if len(item)<=48:
                    file.write("%s\n" % item)
                else:
                    file.write("%.48s...\n" % item)

        with open ('tasks/user.txt', "a", encoding='utf=8') as file:
            file.write(f"\nОставшиеся задачи ({not_done}):\n")

        #Вывод списка с незавершёнными задачами
        with open ('tasks/user.txt', "a", encoding='utf=8') as file:
            for item in not_done_array:
                if len(item)<=48:
                    file.write("%s\n" % item)
                else:
                    file.write("%.48s...\n" % item)

    #Переименование файла по username пользователя
    try:
        default_file = 'tasks/user.txt'
        nikname_file = 'tasks/'+nickname+'.txt'
        old_nikname_file = 'tasks/old_'+nickname+'_'+now_name+'.txt'
        renames(default_file,nikname_file) 
    except :
        renames(nikname_file,old_nikname_file) 
        renames(default_file,nikname_file) 


if __name__ == "__main__":
    while n <=max_id:
        start()
        n+=1    
