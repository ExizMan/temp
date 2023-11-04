import requests
import json
import time
import copy

class DataApi:
    data = []
    def __init__(self, url,show=False):
        '''
                :param URL: str
                :returns: dict with group
        '''
        self._url = url
        is_loaded = False
        print(f"начинаем попытку подключения к {self._url} \n")
        while not is_loaded:
            try:
                response = requests.get(self._url, timeout=10)
                response.raise_for_status()
                is_loaded = True
                if show:
                    print(response.text)
                self.data = json.loads(response.text)

            except requests.exceptions.HTTPError as e:
                print(f'подключение к {self._url} не произвелось, пробуем еще раз...\n Ошибка {e}')
                time.sleep(3)
            except requests.exceptions.RequestException as e:
                print(f'подключение к {self._url} не произвелось, пробуем еще раз... \n Ошибка: {e}')
                time.sleep(3)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                time.sleep(3)

    def select_related(self, serialized_json, foreign_key : dict, on_val):
        """
            Возвращает джоин по столбцам, указанных в словаре foreign_key по значениию on_val
            :param serialized_json:
            :param foreign_key:
            :param on_val:
            :return:
        """
        user = None
        todos_curr = []
        try:
            for pk, fk in foreign_key.items():
                for item in self.data:
                    if item[pk] == on_val:
                        user = copy.copy(item)

                if user is None:
                    raise Exception("значения, по которому вы хотите соединить таблицы, не существует")

                for item in copy.deepcopy(serialized_json):
                    if item.get(fk, None) == on_val:
                        item.pop(fk)
                        todos_curr.append(item)
                user.setdefault("tasks", todos_curr)
                return user

        except Exception as e:
            print(f"Ошибка: {e}")
            return None













