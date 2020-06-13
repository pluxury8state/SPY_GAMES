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
        'access_token': Url,
        'v' : 5.89,
        'filter': 'friends'
    }
    return params
#
# OAUTH = 'https://oauth.vk.com/authorize'                  #
# params = {                                                #
#     'client_id' : 7508353,                                #
#     'redirect_uri': 'https://oauth.vk.com/blank.html',    #
#     'display': 'popup',                                   #
#     'scope':'friends,groups',                             #
#     'response_type' : 'token',                            #       запрос на токен
#     'v' : 5.89                                            #
# }                                                         #
#                                                           #
# URL_to_get_token = ('?'.join((OAUTH,urlencode(params))))  #
#                                                           #
# print(URL_to_get_token)                                   #


#
# class Groups_without_friends:
#     def __init__(self,user_id):
#         self.user_id = user_id



Url = '46eb56cf943b0e8ad9919e590eb506ed399bc921b41072131185f74d978c30f926b68d6a20fdeba715fca' #14:49  # сам токен
params = {
    'access_token': Url,
    'extended': 1,
    'fields':'id,name,members_count',
    'v' : 5.89,
}
#
response = requests.get('https://api.vk.com/method/groups.get',params )         # получаю ответ от сервера с помощью метода get

# pprint(response.json())


answer_get = (response.json()['response'])
counter = 0
mas1 = []

for i in answer_get['items']:   #
    mas1.append(to_output(i))   #    добавление в массив списков данных через ключи:  ['name_group']-> сюда идет название группы
    counter += 1                #                                                     ['id_group']-> сюда идет id группы
                                #                                                     ['members_count'] -> сюда идет число участников  группы
                                #    идет подсчет числа групп для подсчета(counter)





print(f'всего групп у пользователя:{counter}')





mas = []
# в этом месте необходимо провести оптимизацию , т.к времени уходит очень много на запросы
for ind in mas1:



    i = (requests.get('https://api.vk.com/method/groups.getMembers', friends_in_groups(ind['id_group'])))

    if counter != 1:
        print(f'...  осталось запрросить  {counter-1} групп ' )
        counter -= 1
    else:
        print('это окончательный запрос группы')

    time.sleep(0.4)

    count_friends_in_groups = i.json()['response']['count']  # получаем число друзей в группе

    if count_friends_in_groups == 0:  # если число друзей в группе равно 0 , то добавляем id этой группы в массив
        mas.append(ind['id_group'])






mas2 = []

for id_without_friends in mas:                      #
    for i in mas1:                                  #  если id из массива mas  совпадает с id из массива списков mas1, то
        if i['id_group'] == id_without_friends:     #  мы записываем словарь с нужным id в новый массив mas2
                                                    #
            mas2.append(i)                          #
            break                                   #


pprint(mas2)


with open('groups.json','w',encoding='utf-8') as file:  # записываем значения в json file
    json.dump(mas2,file,ensure_ascii=False,indent=2)    #


print('\n\n\n\nготовые ссылки на группы без друзей:\n')
for i in mas2:
    print('https://vk.com/public'+str(i['id_group']))