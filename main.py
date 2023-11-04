from pathlib import Path
import os
import json
import requests
import time
from modules.API_med import DataApi
from modules.IO_med import UserTasks
#from shell import init_dir


usersURL = ('https://json.medrocket.ru/users')
todosURL = ('https://json.medrocket.ru/todos')

command_dict ={""}








def init_dir():
    d1, d2 = DataApi(usersURL), DataApi(todosURL)
    users_tasks = []

    for item in d1.data:
        users_tasks.append(UserTasks(d1.select_related(d2.data, {"id": "userId"}, item["id"])))

    for i in range(len(users_tasks)):
        users_tasks[i].write_reports()


def main():
    Path("tasks").mkdir(parents=True, exist_ok=True)
    init_dir()
    repeat = False
    if input("Если хотите повторить, введите y \n")=='y':
        repeat = True

    while repeat:
        init_dir()
        if input("Если хотите повторить, введите y \n") != 'y':
            repeat = False






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
