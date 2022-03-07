import datetime
import json
import requests
from progress.bar import Bar


class Vk:
    url = 'https://api.vk.com/method/'

    def __init__(self, token: str):
        self.params = {
            'access_token': token,
            'v': '5.131'
        }

    def photos_get(self, owner_id, count_photo):
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': '1',
            'count': count_photo
        }
        if owner_id == '':
            photos_get_params = {
                'album_id': 'profile',
                'extended': '1',
                'count': count_photo
            }

        res = requests.get(url=photos_get_url, params={**self.params, **photos_get_params}).json()
        return res

    def users_get(self, id_owner: str):
        user_get_url = self.url + 'users.get'
        user_get_params = {'user_ids': id_owner}
        if id_owner == '':
            user_get_params = {}
        res = requests.get(url=user_get_url, params={**self.params, **user_get_params}).json()
        return res


class Ya:
    def __init__(self, token: str):
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'OAuth {}'.format(token)
        }

    def upload_post(self, web_url: str, name_file: str, path: str):
        upload_post_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        upload_post_headers = self.headers
        upload_post_params = {
            'path': f'{path}/{name_file}.jpg',
            'url': web_url,
            'overwrite': 'True'
        }
        if path == '':
            upload_post_params = {
                'path': f'{name_file}.jpg',
                'url': web_url,
                'overwrite': 'True'
            }
        requests.post(url=upload_post_url, headers=upload_post_headers, params=upload_post_params)

    def create_folder(self, path: str):
        create_folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        create_folder_headers = self.headers
        create_folder_params = {'path': path}
        requests.put(url=create_folder_url, headers=create_folder_headers, params=create_folder_params)


def upload(path, count, user_id):
    info = vk_token.photos_get(owner_id=user_id, count_photo=count)['response']['items']
    photo = {}

    for dict_ in info:
        date = datetime.datetime.fromtimestamp(dict_['date']).strftime('%Y-%m-%d')
        likes = dict_['likes']['count']
        size = dict_['sizes'][-1]['type']
        url = dict_['sizes'][-1]['url']
        if likes not in photo.keys():
            photo[likes] = {'date': date, 'url': url, 'size': size}
        else:
            photo[f'{likes} {date}'] = {'url': url, 'size': size}

    ya_token.create_folder(path=path)
    with open('Vk_photo_info.json', 'w') as f:
        photo_json = []
        for name, url in Bar('Processing').iter(photo.items()):
            ya_token.upload_post(web_url=url['url'], name_file=name, path=path)
            photo_json.append({'file_name': f'{name}.jpg', 'size': url['size']})
        json.dump(photo_json, f, ensure_ascii=False)
    print('Загрузка прошла успешно!!!')


with open('', encoding='utf8') as vktoken:
    vk_token = Vk(vktoken.readline().strip())

ya_token = Ya(input('Введите токен Яндекс.Диска '))
while True:
    user_id = input('Введите id пользователя VK (по умолчанию владелец токена): ')
    if not vk_token.users_get(f'{user_id}')['response']:
        print('Пользователь с таким id не найден, попробуйте снова')
        continue
    else:
        break
print(f'Количество фотографий в профиле - {vk_token.photos_get(owner_id=user_id, count_photo=1)["response"]["count"]}')
count = input('Введите количество фотографий для копирования (по умолчанию 5): ')
if count == '':
    count = '5'
upload(count=count, user_id=user_id, path='VkPhotoProfileBackup')
