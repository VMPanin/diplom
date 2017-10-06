import requests
import time
import json


token = os.getenv('token_vk_diplom')
VERSION = '5.67'
user_id = input('Введите id пользователя (ex. 5030613):')


def get_my_groups():
    """
    получаем группы друзей пользователя в двух списках:
    - полные данные о группах
    - только id группы
    """
    params = {
        'access_token': token,
        'v': VERSION,
        'user_id': user_id,
        'count': 1000,
        'extended': 1,
        'fields': 'members_count'
    }
    response = requests.get('https://api.vk.com/method/groups.get', params)
    groups_list = response.json()['response']['items']
    print("...")
# Создаем список только id групп
    group_list_id = []
    for group in groups_list:
        group_list_id.append(group['id'])

    return groups_list, group_list_id


def get_my_friends():
    params = {
        'access_token': token,
        'v': VERSION,
        'user_id': user_id,
    }
    print("...")
    response = requests.get('https://api.vk.com/method/friends.get', params)
    friend_list = response.json()['response']['items']
    print("...")
    return friend_list


def get_group_list():
    friend_list = get_my_friends()
    all_groups = []
    try:
        for friend in friend_list:
            print("...")
            params = {'access_token': token,
                      'v': VERSION,
                      'user_id': friend,
                      }
            group_list = requests.get('https://api.vk.com/method/groups.get',
                                      params)
            all_groups.append(group_list.json()['response']['items'])
            time.sleep(0.4)
    except KeyError:
        for friend in friend_list:
            print("...")
            params = {'access_token': token,
                      'v': VERSION,
                      'user_id': friend,
                      }
            group_list = requests.get('https://api.vk.com/method/groups.get',
                                      params)
            time.sleep(0.4)
    return all_groups


def get_target_groups():
    """
    просто находим целевое множество id групп
    """
    all_groups_of_users = get_group_list()
    sum_of_all_groups = sum(all_groups_of_users, [])
    unique_groups = set(sum_of_all_groups)
    set_of_groups_target_user = set(get_my_groups()[1])
    target_groups = set_of_groups_target_user.difference(unique_groups)

    return target_groups


def get_target_group_for_json():
    """
    Подготовим список для сохранения в файл
    """
    groups_of_target_user = get_my_groups()[0]
    target_groups = get_target_groups()
    final_groups = []
    for group in target_groups:
        for group1 in groups_of_target_user:
            if group == group1['id']:
                final_groups.append(group1)

    all_groups_for_json = list()
    for group in final_groups:
        result = {
            'name': group['name'],
            'gid': group['id'],
            'member_count': group['members_count']
        }
        all_groups_for_json.append(result)

    return all_groups_for_json


def save_json():
    with open('groups.json', 'w', encoding='utf8') as f:
        json.dump(get_target_group_for_json(), f, indent=1, ensure_ascii=False)


save_json()
