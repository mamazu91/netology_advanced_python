import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from enum import Enum
from typing import Optional
from vk import match, user
import random
from db import query
from pathlib import Path


class State(Enum):
    GET_USER_TOKEN = -1
    INIT = 0
    GET_USER_INFO = 1
    BDATE_MISSING = 2
    CITY_MISSING = 3
    SEX_MISSING = 4
    SEND_MATCHES = 5


GROUP_TOKEN_FILE = 'group_token.txt'


def get_group_token(group_token_file: str) -> Optional[str]:
    group_token_file_path = Path(__file__).parent / f'../vk/{group_token_file}'

    try:
        with group_token_file_path.open('r', encoding='UTF-8') as file:
            group_token = file.readline()
    except FileNotFoundError:
        print(f'File with group token ({GROUP_TOKEN_FILE}) is missing.')
        exit()
    else:
        return group_token if group_token else None


def is_token_valid(token: str) -> Optional[bool]:
    if token:
        return len(token) == 85


vk_group_token = get_group_token(GROUP_TOKEN_FILE)

if not is_token_valid(vk_group_token):
    print(f'Group token is invalid.')
    exit()

if not vk_group_token:
    print(f'Could not find group token in file {GROUP_TOKEN_FILE}.')
    exit()

vk_group = vk_api.VkApi(token=vk_group_token)
longpoll = vk_api.longpoll.VkLongPoll(vk_group)


def send_message(user_id: int, message: str, attachment=None) -> None:
    vk_group.method(
        'messages.send',
        {'user_id': user_id,
         'random_id': random.randrange(10 ** 7),
         'message': message,
         'attachment': attachment
         }
    )


def send_matches() -> None:
    bot_state = State.GET_USER_TOKEN
    user_info = {}
    vk_user = ''

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                user_id = event.user_id
                user_message = event.text

                if bot_state.value == -1:
                    user_token = user_message

                    if not is_token_valid(user_token):
                        send_message(user_id, 'Введите пользовательский токен.')

                    else:
                        send_message(user_id, 'Токен принят.')
                        send_message(user_id, 'Введите "начать", чтобы начать работу с ботом.')
                        vk_user = vk_api.VkApi(token=user_token)
                        bot_state = State.INIT

                elif bot_state.value == 0:
                    if user_message.lower() == 'начать':
                        send_message(user_id, 'Для кого искать пару? Введите ник или айди пользователя.')
                        bot_state = State.GET_USER_INFO

                    else:
                        send_message(user_id, 'Введите "начать", чтобы начать работу с ботом.')

                elif bot_state.value == 1:
                    send_message(user_id, f'Ищу необходимую информацию по пользователю {user_message}.')
                    user_info = user.get_profile_info(vk_group, user_message)

                    if not user_info:
                        send_message(user_id, 'Не удалось найти указанного пользователя. Повторите ввод.')

                    elif None in user_info.values():
                        send_message(user_id, 'Информация не найдена частично или полностью.')
                        send_message(user_id, 'Введите возраст пользователя.')
                        bot_state = State.BDATE_MISSING

                    else:
                        bdate_without_year_len = 5

                        if len(user_info['bdate']) <= bdate_without_year_len:
                            send_message(user_id, 'Год рождения не указан. Введите возраст пользователя.')
                            bot_state = State.BDATE_MISSING

                        else:
                            user_info['bdate'] = user.calculate_age(user_info['bdate'])
                            send_message(user_id, 'Найдена вся необходимая информация.')
                            send_message(user_id, 'Для начала поиска пар введите любой символ.')
                            bot_state = State.SEND_MATCHES

                elif bot_state.value == 2:
                    try:
                        user_age = int(user_message)
                    except ValueError:
                        send_message(event.user_id, 'Введенное значение некорректно. Повторите ввод.')
                    else:
                        send_message(event.user_id, 'Введен корректный возраст.')
                        user_info['bdate'] = user_age

                        if None in user_info.values():
                            send_message(event.user_id, 'Введите город пользователя.')
                            bot_state = State.CITY_MISSING
                        else:
                            send_message(user_id, 'Найдена вся необходимая информация.')
                            send_message(user_id, 'Для начала поиска пар введите любой символ.')
                            bot_state = State.SEND_MATCHES

                elif bot_state.value == 3:
                    user_city = user.get_city_id(vk_user, user_message)

                    if not user_city:
                        send_message(user_id, f'Указанный город не найден. Повторите ввод.')

                    else:
                        send_message(event.user_id, 'Введен корректный город.')
                        send_message(event.user_id, 'Введите пол пользователя (м/ж).')
                        user_info['city'] = user_city
                        bot_state = State.SEX_MISSING

                elif bot_state.value == 4:
                    user_sex = user_message.lower()

                    if user_sex not in ('м', 'ж'):
                        send_message(event.user_id, 'Неверный пол. Введите "м" или "ж".')

                    else:
                        user_info['sex'] = 2 if user_sex == 'м' else 1
                        send_message(user_id, 'Введен корректный пол.')
                        send_message(user_id, 'Найдена вся необходимая информация.')
                        send_message(user_id, 'Для начала поиска пар введите любой символ.')
                        bot_state = State.SEND_MATCHES

                elif bot_state.value == 5:
                    match_ids = match.get_match_ids(vk_user,
                                                    user_info['city'],
                                                    user_info['sex'],
                                                    user_info['bdate']
                                                    )

                    if not match_ids:
                        send_message(user_id, 'Не удалось найти людей по указанным критериям. '
                                              'Введите "начать", чтобы начать заново.')
                        bot_state = State.INIT

                    else:
                        if query.get_user(user_id):
                            print(f'User {user_id} already in the DB. Skipping its insert.')

                        else:
                            query.insert_user(str(user_id))

                        matches_to_send = 0

                        for i in match_ids:
                            if matches_to_send == 3:
                                break

                            match_id = random.choice(match_ids)
                            db_match_ids = query.get_matches(user_id)

                            if match_id in db_match_ids:
                                print(f'Match with id {match_id} was already sent. Trying another one.')
                                continue

                            match_photo_ids = match.get_match_photo_ids(vk_user, match_id)

                            if not match_photo_ids:
                                print(f'Found a match with id {match_id}, but it does not have any photos. '
                                      f'Trying another one.')
                                continue

                            query.insert_match(match_id, user_id)
                            send_message(user_id, f'Пара найдена. Доступно {len(match_photo_ids[match_id])} фото.')
                            send_message(user_id, f'https://vk.com/id{match_id}')

                            for photo_id in match_photo_ids[match_id]:
                                attachment = f'photo{match_id}_{photo_id}'
                                send_message(user_id, '', attachment=attachment)

                            matches_to_send += 1

                        send_message(user_id,
                                     'Работа бота закончена. Введите "начать", чтобы начать работу с ботом.')
                        bot_state = State.INIT
