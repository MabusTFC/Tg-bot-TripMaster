import { cityCoordinates } from './config.js';


const SWIPE_THRESHOLD = 50; // Порог в пикселях, чтобы жест считался "свайпом"
const SERVER_URL = 'https://6660-45-8-147-174.ngrok-free.app'; // Замените на актуальный ngrok-URL// URL вашего сервера


function getUserId() {
    const isTelegramWebApp = window.Telegram && window.Telegram.WebApp;
    if (isTelegramWebApp) {
        return window.Telegram.WebApp.initDataUnsafe?.user?.id || null;
    }
    const params = new URLSearchParams(window.location.search);
    return params.get("user_id") || '12345';
}

// Функция для генерации случайного цвета
function getRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

// Функция для формирования основной информации о маршруте
function getRouteSummary(routeData) {
  const routeDescription = routeData.route.join(' → ');
  return `
    <b>Маршрут:</b> ${routeDescription}<br>
    <b>Общая цена:</b> ${routeData.total_price} руб.<br>
    <b>Общая длительность:</b> ${routeData.total_duration.toFixed(2)} часов<br>
  `;
}

// Функция для формирования детальной информации о маршруте
function getDetailedRouteInfo(routeData) {
  let detailedInfo = '';

  // Добавляем информацию о первом городе
  detailedInfo += `<div class="step"><span class="step-city">${routeData.route[0]}</span></div>`;

  // Проходим по всем сегментам маршрута (перелётам)
  routeData.full_path.forEach((segment, index) => {
    // Добавляем информацию о перелёте
    detailedInfo += `
      <div class="step">
        <span class="step-flight">
          <b>Перелёт:</b> ${segment.origin} → ${segment.destination}<br>
          Рейс: ${segment.flight_number}<br>
          Отправление: ${new Date(segment.departure_datetime).toLocaleString()}<br>
          Прибытие: ${new Date(segment.arrival_datetime).toLocaleString()}<br>
          Цена: ${segment.price} руб.<br>
          Длительность: ${segment.duration_hours.toFixed(2)} часов
        </span>
      </div>
    `;

    // Добавляем информацию о следующем городе (кроме последнего шага)
    if (index < routeData.route.length - 1) {
      detailedInfo += `<div class="step"><span class="step-city">${routeData.route[index + 1]}</span></div>`;
    }
  });

  return detailedInfo;
}


async function initMap() {
  try {
    let routes = [];

    // Определение, запущено ли приложение в Telegram
    const userId = getUserId();
    routes = await fetchUserRoutes(userId);


    if (!routes || routes.length === 0) {
      throw new Error('Маршруты не найдены');
    }

    // Создание карты Leaflet
    const map = L.map('map').setView([55.7558, 37.6173], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    // Отрисовка городов
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

    // Создание массива цветов для маршрутов
    const routeColors = routes.map(() => getRandomColor());
    // Отрисовка маршрутов
    const routePolylines = [];
    routes.forEach((routeData, index) => {
      const fullPath = routeData.full_path;
      const polylines = [];
      const routeColor = routeColors[index]; // Уникальный цвет для текущего маршрута

      fullPath.forEach(segment => {
        const origin = segment.origin;
        const destination = segment.destination;
        const coordsOrigin = cityCoordinates[origin];
        const coordsDest = cityCoordinates[destination];

        if (coordsOrigin && coordsDest) {
          const polyline = L.polyline([coordsOrigin, coordsDest], {
            color: routeColor,
            weight: 3,
            opacity: index === 0 ? 1 : 0.5 // Первый маршрут более яркий
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

    // Заполняем выпадающий список
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
      const selectedRoute = routes[selectedIndex];

      // Обновляем полилайны на карте
      routePolylines.forEach((polylines, i) => {
        polylines.forEach(polyline => {
          polyline.setStyle({
            color: routeColors[i], // Используем уникальный цвет для маршрута
            weight: i === selectedIndex ? 9 : 3, // Увеличенная толщина для выбранного маршрута
            opacity: i === selectedIndex ? 1 : 0.3, // Выбранный маршрут более яркий
            dashArray: i === selectedIndex ? '5, 5' : null // Пунктирная линия для выбранного маршрута
          });
        });
      });

      // Заполняем основную информацию о маршруте
      document.getElementById('route-summary').innerHTML = getRouteSummary(selectedRoute);

      // Заполняем детальную информацию о маршруте
      document.getElementById('route-detailed-info').innerHTML = getDetailedRouteInfo(selectedRoute);
    });

    // Утилита для програмного выбора маршрута
    function selectRoute(index) {
      routeSelect.value = index;
      routeSelect.dispatchEvent(new Event('change'));
    }

    // Кнопки "Самый дешевый" и "Самый короткий"
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

    // Фильтры по цене и дате
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

    // Мобильная логика: панель и кнопка
    const toggleButton = document.getElementById('toggle-filters');
    const controls = document.getElementById('controls');

    toggleButton.addEventListener('click', () => {
      controls.classList.toggle('open');
      toggleButton.classList.toggle('open');
    });

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

      if (!controls.classList.contains('open') && diff < -SWIPE_THRESHOLD) {
        controls.classList.add('open');
        toggleButton.classList.add('open');
      } else if (controls.classList.contains('open') && diff > SWIPE_THRESHOLD) {
        controls.classList.remove('open');
        toggleButton.classList.remove('open');
      }
    }, { passive: true });

   document.getElementById('export-pdf').addEventListener('click', async () => {
      try {
        const selectedRouteIndex = parseInt(document.getElementById('route-select').value);
        const selectedRoute = routes[selectedRouteIndex];
        const userId = getUserId();

        if (!selectedRoute) {
          alert('Выберите маршрут перед экспортом.');
          return;
        }

        // Создаем PDF с помощью jsPDF
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        // Заголовок
        doc.setFontSize(20);
        doc.text('Маршрут путешествия', 105, 20, { align: 'center' });

        // Информация о маршруте
        doc.setFontSize(12);
        doc.text(`Маршрут: ${selectedRoute.route.join(' → ')}`, 14, 30);
        doc.text(`Общая цена: ${selectedRoute.total_price} руб.`, 14, 40);
        doc.text(`Общая длительность: ${selectedRoute.total_duration.toFixed(2)} часов`, 14, 50);

        // Таблица с сегментами маршрута
        const headers = [["Отправление", "Прибытие", "Откуда", "Куда", "Рейс", "Цена", "Длительность"]];
        const rows = selectedRoute.full_path.map(segment => [
          new Date(segment.departure_datetime).toLocaleString(),
          new Date(segment.arrival_datetime).toLocaleString(),
          segment.origin,
          segment.destination,
          segment.flight_number,
          `${segment.price} руб.`,
          `${segment.duration_hours.toFixed(2)} ч.`
        ]);

        doc.autoTable({
          startY: 60,
          head: headers,
          body: rows,
          theme: 'grid',
          headStyles: {
            fillColor: [100, 100, 100],
            textColor: 255,
            fontStyle: 'bold'
          },
          styles: {
            cellPadding: 3,
            fontSize: 10,
            valign: 'middle'
          },
          columnStyles: {
            0: { cellWidth: 40 },
            1: { cellWidth: 40 },
            2: { cellWidth: 30 },
            3: { cellWidth: 30 },
            4: { cellWidth: 30 },
            5: { cellWidth: 25 },
            6: { cellWidth: 25 }
          }
        });

        // Генерируем PDF
        const pdfBlob = doc.output('blob');
        const formData = new FormData();
        formData.append('document', pdfBlob, 'travel_route.pdf');
        formData.append('chat_id', userId);

        // Отправляем PDF через Telegram Bot API
        const BOT_TOKEN = '7796170704:AAH8La6nGTCf_zd_KrHMSJObrQ5P4HYuMT4';
        const response = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendDocument`, {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error('Не удалось отправить PDF');
        }

        alert('PDF успешно отправлен! Проверьте чат с ботом.');

        if (window.Telegram?.WebApp?.close) {
          window.Telegram.WebApp.close();
        }

      } catch (error) {
        console.error('Export failed:', error);
        alert('Ошибка: ' + error.message);
      }
    });


  } catch (error) {
    console.error('Ошибка при инициализации карты:', error);
  }
}


// Функция для получения маршрутов пользователя
async function fetchUserRoutes(userId) {
  try {
    const url = `${SERVER_URL}/api/routes?user_id=${userId}`;
    console.log('Отправляю запрос:', url);

    // Добавляем заголовок ngrok-skip-browser-warning

    const response = await fetch(url, {
      headers: {
        'ngrok-skip-browser-warning': 'true', // Этот заголовок игнорирует предупреждение ngrok
      },
    });

    if (!response.ok) {
      const errorMessage = await response.text();
      throw new Error(`HTTP ошибка (${response.status}): ${errorMessage}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Ошибка при получении маршрутов:', error);
    return [];
  }
}
document.addEventListener("DOMContentLoaded", initMap);
