from datetime import datetime
import requests


def create_ya_disk_folder(token):
    headers = {
        'authorization': token
    }
    params = {
        'path': f"w6_t2_{str(datetime.now().strftime('%d%m%Y_%H%M%S'))}"
    }
    create_folder_api = 'https://cloud-api.yandex.net/v1/disk/resources'

    create_folder_api_response = requests.put(create_folder_api, headers=headers, params=params)

    if create_folder_api_response.status_code != 201:
        return {
            'status_code': create_folder_api_response.status_code,
            'error_code': create_folder_api_response.json()['error'],
            'error_message': create_folder_api_response.json()['message']
        }

    return params['path']
