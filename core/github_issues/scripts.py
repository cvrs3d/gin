import requests
from core.core.settings import AUTH_TOKEN


class Cursor:
    headers = {'Authorization': f'Bearer {AUTH_TOKEN}'}

    def get_label_list(self, url) -> dict:

        url = url
        labels = []
        page = 1
        index = 1
        result = dict()

        while True:
            response = requests.get(url, params={'page': page})
            if response.status_code != 200:
                print(f"Ошибка при выполнении запроса: {response.status_code}")
                break
            data = response.json()
            if not data:
                break
            labels.extend(data)
            page += 1

        # Выводим полный список меток
        for label in labels:
            result[str(index)] = label['name']
            index += 1

        return result
