import requests
from pprint import pprint
import time
from urllib.parse import urlencode
import json

def to_output(ob):
    output_dict = {}
    output_dict['name_group'] = ob['name']
    output_dict['id_group'] = ob['id']
    output_dict['members_count'] = ob['members_count']
    return output_dict

def friends_in_groups(id):

    params = {
        'group_id': str(id),
        'access_token': Token,
        'v' : 5.89,
        'filter': 'friends'
    }
    return params


class Groups_without_friends:
    def __init__(self,user_id,token):
        self.user_id = user_id
        self.v = 5.89
        self.token = token

    def get_groups(self):
        params = {
            'user_id': self.user_id,
            'access_token': self.token,
            'extended': 1,
            'fields': 'id,name,members_count',
            'v': self.v,
        }
        response = requests.get('https://api.vk.com/method/groups.get',params)  # получаю ответ от сервера с помощью метода get

        answer_get = response.json()['response']
        counter = 0
        mas1 = []

        for i in answer_get['items']:  #
            mas1.append(to_output(i))  # добавление в массив списков данных через ключи:  ['name_group']-> сюда идет название группы
            counter += 1  # ['id_group']-> сюда идет id группы
            #                                                     ['members_count'] -> сюда идет число участников  группы
            #    идет подсчет числа групп для подсчета(counter)
        self.mas1 = mas1
        self.counter = counter
        return mas1

    def get_Members(self):

        mas = []
        # в этом месте необходимо провести оптимизацию , т.к времени уходит очень много на запросы
        for ind in self.mas1:

            i = (requests.get('https://api.vk.com/method/groups.getMembers', friends_in_groups(ind['id_group'])))

            if self.counter != 1:
                print(f'...  осталось запрросить  {self.counter - 1} групп ')
                self.counter -= 1
            else:
                print('это окончательный запрос группы')

            time.sleep(0.4)

            count_friends_in_groups = i.json()['response']['count']  # получаем число друзей в группе

            if count_friends_in_groups == 0:  # если число друзей в группе равно 0 , то добавляем id этой группы в массив
                mas.append(ind['id_group'])


        return mas

    def get_groups_without_friends(self,mas1,mas):
        mas2 = []

        for id_without_friends in mas:  #
            for i in mas1:  # если id из массива mas  совпадает с id из массива списков mas1, то
                if i['id_group'] == id_without_friends:  # мы записываем словарь с нужным id в новый массив mas2
                    #
                    mas2.append(i)  #
                    break  #

        return mas2

Token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008' #'46eb56cf943b0e8ad9919e590eb506ed399bc921b41072131185f74d978c30f926b68d6a20fdeba715fca'

id = input('введите id пользователя:')#281813247

Obj1 = Groups_without_friends(id,Token)

mas1 = Obj1.get_groups()

mas = Obj1.get_Members()


with open('groups.json', 'w', encoding='utf-8') as file:  # записываем значения в json file
    json.dump(Obj1.get_groups_without_friends(mas1,mas), file, ensure_ascii=False, indent=2)  #

        





