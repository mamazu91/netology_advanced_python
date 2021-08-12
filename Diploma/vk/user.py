import vk_api
from datetime import date, datetime
from typing import Optional


def calculate_age(user_birth_date: str) -> int:
    birth_date = datetime.strptime(user_birth_date, '%d.%m.%Y')
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def get_city_id(vk: vk_api.VkApi, user_city: str) -> Optional[int]:
    COUNTRY_ID = 1

    city_id = vk.method(
        'database.getCities',
        {
            'country_id': COUNTRY_ID,
            'q': user_city
        }
    )

    return city_id['items'][0]['id'] if city_id['items'] else None


def get_profile_info(vk_group: vk_api.VkApi, user_id: str) -> Optional[dict]:
    try:
        user_profile_info = vk_group.method(
            'users.get',
            {
                'user_ids': user_id,
                'fields': 'bdate, city, relation, sex'
            }
        )
    except vk_api.ApiError:
        pass
    else:
        city = user_profile_info[0].get('city')

        return {
            'bdate': user_profile_info[0].get('bdate'),
            'city': city['id'] if city else None,
            'sex': user_profile_info[0].get('sex')
        }
