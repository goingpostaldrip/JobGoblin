// Инициализация карты с центром на Москве
const map = L.map('map', {
    minZoom: 3,
    maxZoom: 8,
    center: [56.5, 37.6], // Центр между Москвой и Питером
    zoom: 5, // Увеличиваем zoom чтобы было видно Москву и Питер
    zoomControl: false,
    attributionControl: false,
    dragging: true,
    scrollWheelZoom: true
});

// Создаем минималистичный темный слой карты
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
    attribution: '',
    subdomains: 'abcd',
    maxZoom: 8
}).addTo(map);

// Функция для создания цвета в зависимости от количества вакансий
function getColorByVacancyCount(count) {
    if (count <= 3) return '#6e3bce';
    if (count <= 5) return '#9e3bce';
    return '#c23bb4';
}

// Крупнейшие города Европы и Азии с желтыми кружочками
const majorCities = [
    { name: "Москва", coords: [55.7558, 37.6173] },
    { name: "Санкт-Петербург", coords: [59.9343, 30.3351] },
    { name: "Лондон", coords: [51.5074, -0.1278] },
    { name: "Берлин", coords: [52.5200, 13.4050] },
    { name: "Париж", coords: [48.8566, 2.3522] },
    { name: "Мадрид", coords: [40.4168, -3.7038] },
    { name: "Рим", coords: [41.9028, 12.4964] },
    { name: "Стамбул", coords: [41.0082, 28.9784] },
    { name: "Киев", coords: [50.4501, 30.5234] },
    { name: "Минск", coords: [53.9045, 27.5615] },
    { name: "Прага", coords: [50.0755, 14.4378] },
    { name: "Варшава", coords: [52.2297, 21.0122] },
    { name: "Вена", coords: [48.2082, 16.3738] },
    { name: "Будапешт", coords: [47.4979, 19.0402] },
    { name: "Афины", coords: [37.9838, 23.7275] },
    { name: "Стокгольм", coords: [59.3293, 18.0686] },
    { name: "Осло", coords: [59.9139, 10.7522] },
    { name: "Хельсинки", coords: [60.1699, 24.9384] },
    { name: "Копенгаген", coords: [55.6761, 12.5683] },
    { name: "Амстердам", coords: [52.3676, 4.9041] },
    { name: "Брюссель", coords: [50.8503, 4.3517] },
    { name: "Пекин", coords: [39.9042, 116.4074] },
    { name: "Токио", coords: [35.6762, 139.6503] },
    { name: "Сеул", coords: [37.5665, 126.9780] },
    { name: "Дели", coords: [28.6139, 77.2090] },
    { name: "Мумбаи", coords: [19.0760, 72.8777] },
    { name: "Дубай", coords: [25.2048, 55.2708] },
    { name: "Тегеран", coords: [35.6892, 51.3890] },
    { name: "Баку", coords: [40.4093, 49.8671] },
    { name: "Ереван", coords: [40.1792, 44.4991] },
    { name: "Тбилиси", coords: [41.7151, 44.8271] },
    { name: "Астана", coords: [51.1694, 71.4491] },
    { name: "Алматы", coords: [43.2220, 76.8512] }
];

// Данные по городам с вакансиями
const citiesWithVacancies = [
    {
        name: "Москва",
        coords: [55.7558, 37.6173],
        vacanciesCount: 7,
        vacancies: [
            { title: "Frontend разработчик (React)", salary: "150 000 - 220 000 руб.", company: "Яндекс", format: "Гибрид" },
            { title: "Backend разработчик (Java)", salary: "180 000 - 250 000 руб.", company: "Тинькофф", format: "Удалённый" },
            { title: "Data Scientist", salary: "170 000 - 230 000 руб.", company: "Сбер", format: "Офис" },
            { title: "DevOps инженер", salary: "200 000 - 280 000 руб.", company: "Ozon", format: "Гибрид" },
            { title: "Fullstack разработчик", salary: "160 000 - 220 000 руб.", company: "МТС", format: "Удалённый" },
            { title: "iOS разработчик", salary: "140 000 - 210 000 руб.", company: "VK", format: "Офис" },
            { title: "Android разработчик", salary: "145 000 - 205 000 руб.", company: "Lamoda", format: "Гибрид" }
        ]
    },
    {
        name: "Санкт-Петербург",
        coords: [59.9343, 30.3351],
        vacanciesCount: 6,
        vacancies: [
            { title: "Frontend разработчик (Vue.js)", salary: "120 000 - 180 000 руб.", company: "JetBrains", format: "Гибрид" },
            { title: "Python разработчик", salary: "130 000 - 190 000 руб.", company: "YADRO", format: "Офис" },
            { title: "QA инженер", salary: "90 000 - 140 000 руб.", company: "Газпромнефть", format: "Удалённый" },
            { title: "Системный архитектор", salary: "220 000 - 300 000 руб.", company: "Лукойл-ИТ", format: "Офис" },
            { title: "Data Engineer", salary: "150 000 - 210 000 руб.", company: "ЦФТ", format: "Гибрид" },
            { title: "UX/UI дизайнер", salary: "110 000 - 160 000 руб.", company: "Контур", format: "Удалённый" }
        ]
    },
    {
        name: "Новосибирск",
        coords: [55.0084, 82.9357],
        vacanciesCount: 4,
        vacancies: [
            { title: "Ruby разработчик", salary: "100 000 - 150 000 руб.", company: "2GIS", format: "Офис" },
            { title: "PHP разработчик", salary: "90 000 - 140 000 руб.", company: "Сибинтек", format: "Гибрид" },
            { title: "C++ разработчик", salary: "120 000 - 170 000 руб.", company: "Новософт", format: "Удалённый" },
            { title: "Бизнес-аналитик", salary: "110 000 - 160 000 руб.", company: "Элтекс", format: "Офис" }
        ]
    },
    {
        name: "Екатеринбург",
        coords: [56.8389, 60.6057],
        vacanciesCount: 5,
        vacancies: [
            { title: "Frontend разработчик (Angular)", salary: "110 000 - 160 000 руб.", company: "СКБ Контур", format: "Гибрид" },
            { title: "Java разработчик", salary: "120 000 - 180 000 руб.", company: "Уралсевербанк", format: "Офис" },
            { title: "Сетевой инженер", salary: "100 000 - 150 000 руб.", company: "Уралхим", format: "Удалённый" },
            { title: "Product Manager", salary: "130 000 - 190 000 руб.", company: "МВидео", format: "Офис" },
            { title: "React Native разработчик", salary: "115 000 - 165 000 руб.", company: "КРОК", format: "Гибрид" }
        ]
    },
    {
        name: "Казань",
        coords: [55.7961, 49.1064],
        vacanciesCount: 3,
        vacancies: [
            { title: "Frontend разработчик", salary: "90 000 - 140 000 руб.", company: "Ак Барс Банк", format: "Офис" },
            { title: ".NET разработчик", salary: "100 000 - 150 000 руб.", company: "Татнефть", format: "Гибрид" },
            { title: "Системный администратор", salary: "80 000 - 120 000 руб.", company: "Казаньоргсинтез", format: "Офис" }
        ]
    }
];

// Добавляем желтые кружочки для крупнейших городов
majorCities.forEach(city => {
    L.circleMarker(city.coords, {
        radius: 3,
        color: '#ffcc00',
        fillColor: '#ffcc00',
        fillOpacity: 1,
        weight: 1
    }).addTo(map);

    // Добавляем подпись города
    L.marker(city.coords, {
        icon: L.divIcon({
            className: 'city-label',
            html: `<div>${city.name}</div>`,
            iconSize: [60, 20],
            iconAnchor: [30, 0]
        })
    }).addTo(map);
});

// Добавляем города с вакансиями
citiesWithVacancies.forEach(city => {
    // Добавляем маркер вакансий
    const vacancyMarker = L.circleMarker([city.coords[0] + 0.25, city.coords[1] + 0.15], {
        radius: 8 + (city.vacanciesCount / 2),
        color: '#ffffff',
        fillColor: getColorByVacancyCount(city.vacanciesCount),
        fillOpacity: 0.9,
        weight: 2,
        className: 'vacancy-marker'
    }).addTo(map);

    // Создаем контент для popup
    const popupContent = `
        <div class="vacancy-popup-title">Вакансии в ${city.name}</div>
        <ul class="vacancy-list">
            ${city.vacancies.map(vacancy => `
                <li class="vacancy-item">
                    <div class="vacancy-title">${vacancy.title}</div>
                    <div class="vacancy-salary">${vacancy.salary}</div>
                    <div class="vacancy-company">${vacancy.company}</div>
                    <div class="vacancy-format">${vacancy.format}</div>
                </li>
            `).join('')}
        </ul>
    `;

    // Привязываем popup к маркеру
    vacancyMarker.bindPopup(popupContent, {
        maxWidth: 330,
        className: 'vacancy-popup'
    });

    // Обработчик для показа количества вакансий
    vacancyMarker.on('mouseover', function(e) {
        showVacancyCount(city, e.latlng);
    });

    vacancyMarker.on('mouseout', function() {
        hideVacancyCount();
    });
});

// Функция для показа количества вакансий
function showVacancyCount(city, latlng) {
    const countElement = document.getElementById('vacancyCount');
    countElement.textContent = `${city.vacanciesCount} вакансий`;

    const point = map.latLngToContainerPoint(latlng);
    countElement.style.left = (point.x + 15) + 'px';
    countElement.style.top = (point.y - 15) + 'px';
    countElement.style.display = 'block';
}

// Функция для скрытия количества вакансий
function hideVacancyCount() {
    document.getElementById('vacancyCount').style.display = 'none';
}

// Обработчики для вкладок (заглушки)
document.querySelectorAll('.tab.inactive').forEach(tab => {
    tab.addEventListener('click', function() {
        alert('Этот раздел находится в разработке');
    });
});