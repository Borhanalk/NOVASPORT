// إعداد الخريطة
const map = L.map('map').fitWorld();

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

// تحديد موقع المستخدم
map.locate({ setView: true, maxZoom: 16 });

function onLocationFound(e) {
    const radius = e.accuracy / 2;

    // إضافة علامة لموقع المستخدم
    L.marker(e.latlng).addTo(map)
        .bindPopup(`أنت هنا!<br>دقة الموقع: ${radius.toFixed(2)} متر.`).openPopup();

    // إضافة دائرة حول موقع المستخدم
    L.circle(e.latlng, radius, { color: '#008cba' }).addTo(map);
}

map.on('locationfound', onLocationFound);

function onLocationError(e) {
    alert(e.message);
}

map.on('locationerror', onLocationError);

// جلب الأماكن من الخادم
fetch('/locations/locations-json/')
    .then(response => response.json())
    .then(locations => {
        locations.forEach(location => {
            L.marker([location.latitude, location.longitude])
                .addTo(map)
                .bindPopup(`<strong>${location.name}</strong><br>${location.description}`);
        });
    });
