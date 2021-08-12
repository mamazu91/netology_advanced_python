import vk_api
from typing import Optional


def get_match_ids(vk_user: vk_api.VkApi, user_city: int, user_sex: int, user_age: int) -> Optional[list]:
    COUNT = 1000
    STATUS = None
    HAS_PHOTO = 1

    matches = vk_user.method(
        'users.search',
        {
            'count': COUNT,
            'city': user_city,
            'sex': 2 if user_sex == 1 else 1,
            'status': STATUS,
            'age_from': user_age,
            'age_to': user_age,
            'has_photo': HAS_PHOTO
        }
    )

    match_ids = [str(match['id']) for match in matches['items']]

    return match_ids if match_ids else None


def get_match_photo_ids(vk_user: vk_api.VkApi, match_id: str) -> Optional[dict]:
    ALBUM_ID = 'profile'
    EXTENDED = 1

    try:
        album_photos = vk_user.method(
            'photos.get',
            {
                'owner_id': match_id,
                'album_id': ALBUM_ID,
                'extended': EXTENDED
            }
        )
    except vk_api.ApiError as vk_api_error:
        print(f'Skipping profile {match_id} due to an error: {vk_api_error}.')
    else:
        match_photos = {match_id: [photo['id'] for photo in
                                   sorted(album_photos['items'],
                                          key=lambda item: item['likes']['count'] + item['comments']['count'],
                                          reverse=True)[0:3]
                                   ]}

        return match_photos
