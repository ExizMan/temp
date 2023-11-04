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













"""def API_getElem(URLuser: str, URLtodos: str, id_u: int, user_key="id", foreign_key="userId", ) -> dict:
    '''
    Returns joined dict\n
    Возвращает словарь. присоединенный по аргументу
    :param URLuser:
    :param URLtodos:
    :param foreign_key:
    :param user_key:
    :param URL:
    :param id_u:
    :return: dict with user
    '''
    try:
        response_user = requests.get(URLuser, timeout=10)
        print(f'Подключение по {URLuser}')
        response_todos = requests.get(URLtodos, timeout=10)
        print(f'Подключение по {URLtodos}')
        user = next((item for item in json.loads(response_user.text) if item[user_key] == id_u), None)
        todos = json.loads(response_todos.text)

        todos_curr = []
        print(todos)
        for item in todos:
            if item.get(foreign_key, None) == id_u:
                todos_curr.append(item)
        print(todos_curr)
        if len(todos_curr) == 0:
            raise Exception("не найдены задачи по userId")

        if user is None:
            raise Exception("не найден user по id")
        user.setdefault("tasks", todos_curr)
        return user

    except requests.exceptions.RequestException as e:
        print(f'подключение не произвелось, пробуем еще раз... \n Ошибка: {e}')

    except requests.exceptions.HTTPError as e:
        print(f'подключение не произвелось, пробуем еще раз...\n Ошибка {e}')

    # except Exception as e:
    #      print(f"Произошла ошибка: {e}")
    return None
"""

# def API_get(self, show=False):
#     '''
#     Returns dict with values from API response\n
#     Возвращает словарь из API запроса
#     :param URL: str
#     :returns: dict with group
#     '''
#     is_loaded = False
#     while not is_loaded:
#         try:
#             response = requests.get(self._url, timeout=10)
#             response.raise_for_status()
#             is_loaded = True
#             if show:
#                 print(response.text)
#             self.data = json.loads(response.text)
#             return self.data
#
#         except requests.exceptions.RequestException as e:
#             print(f'подключение к {self._url} не произвелось, пробуем еще раз... \n Ошибка: {e}')
#             time.sleep(3)
#
#         except requests.exceptions.HTTPError as e:
#             print(f'подключение к {self._url} не произвелось, пробуем еще раз...\n Ошибка {e}')
#
#         except Exception as e:
#             print(f"Произошла ошибка: {e}")
