// config.js

export const cityCoordinates = {
    "Москва": [55.7558, 37.6173],
    "Казань": [55.7961, 49.1064],
    "Новгород": [58.5215, 31.2758],
    "Санкт-Петербург": [59.9343, 30.3351],
    "Самара": [53.1958, 50.1002],
    "Екатеринбург": [56.8380, 60.5975],
    "Новосибирск": [55.0302, 82.9204]
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