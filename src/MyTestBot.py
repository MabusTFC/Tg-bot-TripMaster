import requests
import json

# Путь к файлу routes.json
file_path = "../docs/routes.json"

# URL сервера
url = "https://6660-45-8-147-174.ngrok-free.app/api/save-routes"

# Чтение данных из файла routes.json
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Добавление user_id в данные
data_with_user_id = {
    "user_id": "12345",
    "routes": data  # Предполагается, что в файле routes.json находится массив маршрутов
}

# Отправка POST-запроса на сервер
response = requests.post(url, json=data_with_user_id)

# Вывод результатов
print("Status Code:", response.status_code)
print("Response Body:", response.json())