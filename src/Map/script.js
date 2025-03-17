// script.js

import { cityCoordinates, routes, loadRoutes } from './config.js';

// Основная функция для инициализации карты и маршрутов
async function initMap() {
    try {
        // Загрузка маршрутов
        await loadRoutes();

        // Создание карты
        const map = L.map('map').setView([55.7558, 37.6173], 5);

        // Добавление тайлов OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap'
        }).addTo(map);

        // Добавляем жирные точки для городов
        Object.keys(cityCoordinates).forEach(city => {
            const coords = cityCoordinates[city];
            L.circleMarker(coords, {
                radius: 8,
                color: "black",
                fillColor: "white",
                fillOpacity: 1
            }).addTo(map)
              .bindTooltip(city, {permanent: true, direction: "top"});
        });

        // Хранилище полилиний для управления их видимостью
        const routePolylines = [];

        // Обработка маршрутов
        routes.forEach((routeData, index) => {
            const fullPath = routeData.full_path;
            const polylines = [];

            fullPath.forEach(segment => {
                const origin = segment.origin;
                const destination = segment.destination;
                const coordsOrigin = cityCoordinates[origin];
                const coordsDest = cityCoordinates[destination];

                if (coordsOrigin && coordsDest) {
                    const polyline = L.polyline([coordsOrigin, coordsDest], {color: index === 0 ? 'blue' : 'green'}).addTo(map);
                    polyline.bindPopup(`
                        <b>Перелет: ${origin} → ${destination}</b><br>
                        Рейс: ${segment.flight_number}<br>
                        Отправление: ${segment.departure_datetime}<br>
                        Прибытие: ${segment.arrival_datetime}<br>
                        Цена: ${segment.price} руб.
                    `);
                    polylines.push(polyline);
                }
            });

            routePolylines.push(polylines);
        });

        // Функция для отображения общей информации о маршруте
        function getRouteInfo(routeData) {
            const routeDescription = routeData.route.join(' → ');

            return `
                <b>Описание маршрута:</b> ${routeDescription}<br>
                <b>Общая информация:</b><br>
                Начало: ${new Date(routeData.start_date).toLocaleString()}<br>
                Конец: ${new Date(routeData.end_date).toLocaleString()}<br>
                Длительность: ${routeData.duration} часов<br>
                Общая цена: ${routeData.total_price} руб.
            `;
        }

        // Заполнение выпадающего списка маршрутами
        const routeSelect = document.getElementById('route-select');
        const infoContainer = document.getElementById('route-info');

        routes.forEach((routeData, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `Маршрут ${index + 1}`;
            routeSelect.appendChild(option);
        });

        // Обработчик выбора маршрута из выпадающего списка
        routeSelect.addEventListener('change', (event) => {
            const selectedIndex = parseInt(event.target.value);

            // Сделать все маршруты тусклыми
            routePolylines.forEach((polylines, i) => {
                polylines.forEach(polyline => polyline.setStyle({opacity: i === selectedIndex ? 1 : 0.3}));
            });

            // Показать информацию о выбранном маршруте
            const selectedRoute = routes[selectedIndex];
            infoContainer.innerHTML = getRouteInfo(selectedRoute);
        });

        // Функция для выбора маршрута в выпадающем списке
        function selectRoute(index) {
            routeSelect.value = index;
            routeSelect.dispatchEvent(new Event('change'));
        }

        // Кнопка "Самый дешевый маршрут"
        document.getElementById('cheapest-route').addEventListener('click', () => {
            const cheapestRoute = routes.reduce((min, route) =>
                route.total_price < min.total_price ? route : min
            );

            alert(`Самый дешевый маршрут: ${cheapestRoute.route.join(' → ')}, цена: ${cheapestRoute.total_price} руб.`);
            selectRoute(routes.indexOf(cheapestRoute));
        });

        // Кнопка "Самый короткий маршрут"
        document.getElementById('shortest-route').addEventListener('click', () => {
            const shortestRoute = routes.reduce((min, route) =>
                route.duration < min.duration ? route : min
            );

            alert(`Самый короткий маршрут: ${shortestRoute.route.join(' → ')}, длительность: ${shortestRoute.duration} часов`);
            selectRoute(routes.indexOf(shortestRoute));
        });

        // Кнопка "Применить фильтры"
        document.getElementById('apply-filters').addEventListener('click', () => {
            const maxPrice = parseFloat(document.getElementById('max-price').value);
            const maxDate = document.getElementById('max-date').value;

            const filteredRoutes = routes.filter(route => {
                const priceCondition = isNaN(maxPrice) || route.total_price <= maxPrice;
                const dateCondition = !maxDate || new Date(route.end_date) <= new Date(maxDate);

                return priceCondition && dateCondition;
            });

            if (filteredRoutes.length === 0) {
                alert('Нет маршрутов, соответствующих фильтрам.');
                return;
            }

            // Очищаем выпадающий список и заполняем его отфильтрованными маршрутами
            routeSelect.innerHTML = '';
            filteredRoutes.forEach((routeData, index) => {
                const option = document.createElement('option');
                option.value = index;
                option.textContent = `Маршрут ${index + 1}`;
                routeSelect.appendChild(option);
            });

            // Выбираем первый маршрут из отфильтрованных
            selectRoute(0);
        });
    } catch (error) {
        console.error('Ошибка при загрузке маршрутов:', error);
    }
}

// Инициализация карты
initMap();