import { cityCoordinates, routes, loadRoutes } from './config.js';

const SWIPE_THRESHOLD = 50; // Порог в пикселях, чтобы жест считался "свайпом"

async function initMap() {
  try {
    // 1. Загрузка маршрутов
    await loadRoutes();

    // 2. Создание карты Leaflet
    const map = L.map('map').setView([55.7558, 37.6173], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    // 3. Отрисовка городов
    Object.keys(cityCoordinates).forEach(city => {
      const coords = cityCoordinates[city];
      L.circleMarker(coords, {
        radius: 8,
        color: "black",
        fillColor: "white",
        fillOpacity: 1
      }).addTo(map)
        .bindTooltip(city, { permanent: true, direction: "top" });
    });

    // 4. Отрисовка маршрутов
    const routePolylines = [];
    routes.forEach((routeData, index) => {
      const fullPath = routeData.full_path;
      const polylines = [];
      fullPath.forEach(segment => {
        const origin = segment.origin;
        const destination = segment.destination;
        const coordsOrigin = cityCoordinates[origin];
        const coordsDest = cityCoordinates[destination];
        if (coordsOrigin && coordsDest) {
          const polyline = L.polyline([coordsOrigin, coordsDest], {
            color: index === 0 ? 'blue' : 'green'
          }).addTo(map);
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

    // Функция для отображения инфо по маршруту
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

    // 5. Заполняем выпадающий список
    const routeSelect = document.getElementById('route-select');
    const infoContainer = document.getElementById('route-info');
    routes.forEach((routeData, index) => {
      const option = document.createElement('option');
      option.value = index;
      option.textContent = `Маршрут ${index + 1}`;
      routeSelect.appendChild(option);
    });

    routeSelect.addEventListener('change', (event) => {
      const selectedIndex = parseInt(event.target.value);
      routePolylines.forEach((polylines, i) => {
        polylines.forEach(polyline => {
          polyline.setStyle({ opacity: i === selectedIndex ? 1 : 0.3 });
        });
      });
      const selectedRoute = routes[selectedIndex];
      infoContainer.innerHTML = getRouteInfo(selectedRoute);
    });

    // Утилита для програмного выбора маршрута
    function selectRoute(index) {
      routeSelect.value = index;
      routeSelect.dispatchEvent(new Event('change'));
    }

    // 6. Кнопки "Самый дешевый" и "Самый короткий"
    document.getElementById('cheapest-route').addEventListener('click', () => {
      const cheapestRoute = routes.reduce((min, route) =>
        route.total_price < min.total_price ? route : min
      );
      alert(`Самый дешевый маршрут: ${cheapestRoute.route.join(' → ')}, цена: ${cheapestRoute.total_price} руб.`);
      selectRoute(routes.indexOf(cheapestRoute));
    });

    document.getElementById('shortest-route').addEventListener('click', () => {
      const shortestRoute = routes.reduce((min, route) =>
        route.duration < min.duration ? route : min
      );
      alert(`Самый короткий маршрут: ${shortestRoute.route.join(' → ')}, длительность: ${shortestRoute.duration} часов`);
      selectRoute(routes.indexOf(shortestRoute));
    });

    // 7. Фильтры по цене и дате
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

      routeSelect.innerHTML = '';
      filteredRoutes.forEach((routeData, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = `Маршрут ${index + 1}`;
        routeSelect.appendChild(option);
      });
      selectRoute(0);
    });

    // 8. Мобильная логика: панель и кнопка
    const toggleButton = document.getElementById('toggle-filters');
    const controls = document.getElementById('controls');

    // --- КЛИК на кнопку: просто открываем/закрываем ---
    toggleButton.addEventListener('click', () => {
      controls.classList.toggle('open');
      toggleButton.classList.toggle('open');
    });

    // --- СВАЙП по ПАНЕЛИ (закрытие) ---
    let panelStartY = 0;
    let panelCurrentY = 0;
    controls.addEventListener('touchstart', (e) => {
      if (!controls.classList.contains('open')) return;
      panelStartY = e.touches[0].clientY;
      panelCurrentY = panelStartY;
    }, { passive: true });

    controls.addEventListener('touchmove', (e) => {
      if (!controls.classList.contains('open')) return;
      panelCurrentY = e.touches[0].clientY;
    }, { passive: true });

    controls.addEventListener('touchend', () => {
      if (!controls.classList.contains('open')) return;
      const diff = panelCurrentY - panelStartY;
      if (diff > SWIPE_THRESHOLD) {
        controls.classList.remove('open');
        toggleButton.classList.remove('open');
      }
    }, { passive: true });

    // --- СВАЙП по КНОПКЕ (и открытие, и закрытие) ---
    let buttonStartY = 0;
    let buttonCurrentY = 0;

    toggleButton.addEventListener('touchstart', (e) => {
      buttonStartY = e.touches[0].clientY;
      buttonCurrentY = buttonStartY;
    }, { passive: true });

    toggleButton.addEventListener('touchmove', (e) => {
      buttonCurrentY = e.touches[0].clientY;
    }, { passive: true });

    toggleButton.addEventListener('touchend', () => {
      const diff = buttonCurrentY - buttonStartY;

      // Если панель закрыта и свайп вверх => ОТКРЫВАЕМ
      if (!controls.classList.contains('open') && diff < -SWIPE_THRESHOLD) {
        controls.classList.add('open');
        toggleButton.classList.add('open');
      }

      // Если панель открыта и свайп вниз => ЗАКРЫВАЕМ
      else if (controls.classList.contains('open') && diff > SWIPE_THRESHOLD) {
        controls.classList.remove('open');
        toggleButton.classList.remove('open');
      }
    }, { passive: true });

  } catch (error) {
    console.error('Ошибка при инициализации карты:', error);
  }
}

initMap();
