// config.js

export const cityCoordinates = {
    "Москва": [55.7558, 37.6173], // Москва
    "Казань": [55.7961, 49.1064], // Казань
    "Новгород": [58.5215, 31.2758], // Великий Новгород
    "Санкт-Петербург": [59.9343, 30.3351], // Санкт-Петербург
    "Самара": [53.1958, 50.1002], // Самара
    "Екатеринбург": [56.8380, 60.5975], // Екатеринбург
    "Новосибирск": [55.0302, 82.9204], // Новосибирск
    "Челябинск": [55.1540, 61.4291], // Челябинск
    "Сочи": [43.6028, 39.7342], // Сочи
    "Владивосток": [43.1154, 131.8855], // Владивосток
    "Ростов-на-Дону": [47.2221, 39.7196], // Ростов-на-Дону
    "Уфа": [54.7388, 55.9711], // Уфа
    "Пермь": [58.0105, 56.2289], // Пермь
    "Омск": [54.9924, 73.3686], // Омск
    "Красноярск": [56.0184, 92.8672], // Красноярск
    "Воронеж": [51.6720, 39.1843], // Воронеж
    "Волгоград": [48.7071, 44.5169] // Волгоград
};

let routes = [];

export async function loadRoutes() {
    try {
        const response = await fetch('./routes.json');
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        routes = await response.json();
        console.log('Маршруты загружены:', routes); // Отладочный вывод
    } catch (error) {
        console.error('Ошибка загрузки маршрутов:', error);
    }
}

export { routes };