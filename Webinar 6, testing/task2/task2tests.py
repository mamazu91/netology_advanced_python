import task2app
import requests


class TestCreateYaDiskFolder:

    def setup_class(self):
        self.token = 'INSERT_YOUR_TOKEN_HERE'
        self.empty_token = None
        self.get_folder_api = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.params = {
            'path': task2app.create_ya_disk_folder(self.token)
        }

    def test_create_ya_disk_folder(self):
        headers = {
            'authorization': self.token
        }

        get_folder_api_status_code = requests.get(
            self.get_folder_api,
            headers=headers,
            params=self.params
        ).status_code

        assert get_folder_api_status_code == 200

    def test_create_ya_disk_folder_unauthorized(self):
        headers = {
            'authorization': self.empty_token
        }

        get_folder_api_status_code = requests.get(
            self.get_folder_api,
            headers=headers,
            params=self.params
        ).status_code

        assert get_folder_api_status_code == 401
