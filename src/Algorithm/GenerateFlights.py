import requests
import json

def fetch_city_codes():
    """
    Получает словарь {название города: код города} через API Яндекс.Расписаний.
    """
    endpoint = "https://api.rasp.yandex.net/v3.0/stations_list/"
    params = {
        "apikey": 'b553ddc4-f6db-4d6e-bc3a-cde7801110c2',  # Ваш API-ключ от Яндекс.Расписаний
        "lang": "ru_RU"
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Проверка на успешный статус запроса
        data = response.json()

        # Создаем словарь {название города: код города}
        city_to_yandex_code = {}
        for country in data.get("countries", []):
            for region in country.get("regions", []):
                for settlement in region.get("settlements", []):
                    city_name = settlement.get("title")
                    codes = settlement.get("codes", {})
                    city_code = codes.get("yandex_code")  # Извлекаем только yandex_code

                    if city_code:  # Добавляем только если код существует
                        city_to_yandex_code[city_name] = city_code

        return city_to_yandex_code
    except requests.RequestException as e:
        print("Ошибка при выполнении запроса к API Яндекс.Расписаний:", e)
        return None

# Получаем словарь городов
city_to_yandex_code = fetch_city_codes()

# Сохраняем в файл
if city_to_yandex_code:
    with open("city_to_yandex_code.json", "w", encoding="utf-8") as file:
        json.dump(city_to_yandex_code, file, ensure_ascii=False, indent=4)
    print("Словарь городов успешно сохранен в файл.")
else:
    print("Не удалось получить данные о городах.")