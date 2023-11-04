from datetime import datetime
import requests
import json
import os

world_time_URL = r'http://worldtimeapi.org/api/timezone/Europe/Moscow'


def private_create_data():
    """
    Получаем время из сети, иначе берем из системы
    :return:
    """
    try:
        response = requests.get(world_time_URL)
        data = json.loads(response.text)
        return datetime.fromisoformat(data['datetime'])
        # print(f"Время полученно из {world_time_URL}")

    except Exception as e:
        print(f"при обращении к {world_time_URL} произошла ошибка {e} \n время будет взято из вашей системы")
        return datetime.now()


class UserTasks:
    user = {}
    tasks = {}
    template = ""

    def __init__(self, user_dict: dict) -> None:
        self.tasks = user_dict.pop('tasks')
        self.user = user_dict
        self.time = private_create_data()


    def __del__(self):
        print("экземпляр удален")

    def _task_constr(self, tasks_list) -> None:
        for item in tasks_list:
            if len(item["title"]) < 47:
                self.template += f"-{item['title']} \n"
            else:
                self.template += f"-{item['title'][0:47]}...\n"

    def template_for_reports(self, return_value=False):
        completed = [item for item in self.tasks if item.get("completed")]
        uncompleted = [item for item in self.tasks if not item.get("completed")]

        self.template = (f"# Отчет для {self.user.get('company').get('name')}. \n"
                         f"{self.user.get('name')} <{self.user.get('email')}> {self.time.strftime('%d.%m.%Y %H:%M')} \n"
                         f"Всего задач:{len(self.tasks)} \n \n")
        if len(uncompleted)>0:
            self.template += (f"## Актуальные задачи {len(uncompleted)} \n")
            self._task_constr(uncompleted)

        if len(uncompleted)>0:
            self.template += (f"\n## Завершенные задачи {len(completed)} \n")
            self._task_constr(completed)

        if return_value: return self.template

    def write_reports(self):
        file_name = f"tasks/{self.user.get('username')}"
        if os.path.exists(file_name):
            # Если файл существует, переименовываем его
            new_name = f"tasks/old_{self.user.get('username')}_{self.time.strftime('%Y-%m-%dT%H:%M')}"
            os.rename(file_name, new_name)
            print(f"Переименовал {file_name} в {new_name}")
        try:
            with open(file_name,'w') as new_report:
                new_report.write(self.template_for_reports(return_value=True))
        except FileNotFoundError:
            print("Папка куда то пропала :/ \n Содаем папку, попробуйте ещё раз! \n")
            os.mkdir("tasks")
        except Exception as e:
            print("Кажется, что то поломалось во время записи на диск \n"
                  f"Ошибка {e}")


