import os
from pprint import pprint
import requests
import time
import pandas as pd


class VK:
    def __init__(self, token: str):
        self.token = token

    def photos_get(self):
        URL = 'https://api.vk.com/method/photos.get'
        param = {
            'access_token': self.token,
            'v': '5.131',
            'album_id': 'profile',
            'count': '50'
        }
        res = requests.get(url=URL, params=param).json()
        return res
        # pprint(res)
        # return res['response']['items']


# class Ya:
#     def __init__(self, token: str):
#         self.token = token
#
#     def upload(self, file_path: str):
#         name_file = os.path.basename(file_path)
#         url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
#         head = {'Accept': 'application/json', 'Authorization': 'OAuth {}'.format(self.token)}
#         param = {'path': '{}'.format(name_file), 'overwrite': 'True'}
#         resp_get = requests.get(url=url, headers=head, params=param).json().get('href')
#         x = requests.put(url=resp_get, headers=head, data=open(file_path))
#         if x.status_code == 201:
#             print('Загрузка прошла успешно!!!')


with open('C:\\Users\\Александр\\Desktop\\vk_token.txt', encoding='utf8') as vktoken:
    vk_token = VK(vktoken.readline().strip())
# vk_token.photos_get()
count = 2
foto = []
while count > 0:
    foto.append(vk_token.photos_get())
    time.sleep(0.35)
    count -= 1
pprint(foto)