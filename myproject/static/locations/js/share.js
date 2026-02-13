// إنشاء الخريطة وتحديد مركزها
const map = L.map('map').setView([31.5, 34.5], 10);

// إضافة خريطة OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// تحديد الموقع الخاص بك
map.locate({ setView: true, maxZoom: 16 });

// إنشاء مجموعات الطبقات
const nearbyFieldsLayer = L.layerGroup().addTo(map);
const allFieldsLayer = L.layerGroup().addTo(map);
const filteredFieldsLayer = L.layerGroup().addTo(map);

// عند العثور على الموقع
map.on('locationfound', async (e) => {
    const userLatLng = e.latlng;

    // إضافة دائرة حمراء تمثل موقعك
    L.circle(userLatLng, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 50 // نصف قطر الدائرة بالمتر
    }).addTo(map).bindPopup("Your Current Location").openPopup();

    // إضافة Marker على الموقع الحالي
    L.marker(userLatLng).addTo(map).bindPopup("Your Current Location").openPopup();

    // 1. جلب المواقع القريبة
    const nearbyFields = await fetchNearbyFields(userLatLng);
    displayLocationsOnMap(nearbyFields, nearbyFieldsLayer, "Nearby Fields");

    // 2. جلب جميع المواقع
    const allFields = await fetchAllFields();
    displayLocationsOnMap(allFields, allFieldsLayer, "All Fields");

    // 3. جلب أسماء المواقع
    const fieldNames = await fetchFieldNames();
    populateFieldNameSuggestions(fieldNames);

    // 4. جلب أنواع الحقول
    const fieldTypes = await fetchFieldTypes();
    populateFieldTypeFilter(fieldTypes);
});

// التعامل مع أخطاء تحديد الموقع
map.on('locationerror', (e) => {
    alert("Unable to locate your position: " + e.message);
});

// دالة لجلب المواقع القريبة
async function fetchNearbyFields(userLatLng) {
    const { lat, lng } = userLatLng;
    const maxDistance = 10; // أقصى مسافة بالكيلومترات

    try {
        const response = await fetch(`/locations/get_nearby_fields?latitude=${lat}&longitude=${lng}&max_distance=${maxDistance}`);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error fetching nearby fields:", error);
        return [];
    }
}

// دالة لجلب جميع المواقع
async function fetchAllFields() {
    try {
        const response = await fetch('/locations/get_field_locations');
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error fetching all fields:", error);
        return [];
    }
}

// دالة لجلب أسماء الحقول
async function fetchFieldNames() {
    try {
        const response = await fetch('/locations/get_field_names');
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error fetching field names:", error);
        return [];
    }
}

// دالة لجلب أنواع الحقول
async function fetchFieldTypes() {
    try {
        const response = await fetch('/locations/get_field_types');
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error fetching field types:", error);
        return [];
    }
}

// دالة لإضافة أسماء المواقع إلى مربع البحث
function populateFieldNameSuggestions(names) {
    const searchBox = document.getElementById('search-box');
    const suggestionsList = document.getElementById('suggestions');

    searchBox.addEventListener('input', () => {
        const query = searchBox.value.toLowerCase();
        suggestionsList.innerHTML = '';

        names
            .filter((name) => name.name.toLowerCase().includes(query))
            .forEach((name) => {
                const li = document.createElement('li');
                li.textContent = name.name;
                suggestionsList.appendChild(li);

                li.addEventListener('click', () => {
                    searchBox.value = name.name;
                    suggestionsList.innerHTML = '';
                });
            });
    });
}

// دالة لإضافة أنواع الحقول إلى قائمة التصفية
function populateFieldTypeFilter(types) {
    const filterSelect = document.getElementById('filter-select');
    types.forEach((type) => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        filterSelect.appendChild(option);
    });

    // إضافة حدث لتصفية الحقول حسب النوع
    filterSelect.addEventListener('change', async (e) => {
        const selectedType = e.target.value;
        const filteredFields = await fetchFilteredFields(selectedType);
        displayLocationsOnMap(filteredFields, filteredFieldsLayer, "Filtered Fields");
    });
}

// دالة لجلب الحقول حسب النوع
async function fetchFilteredFields(fieldType) {
    try {
        const response = await fetch(`/locations/locations_json?type=${fieldType}`);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error fetching filtered fields:", error);
        return [];
    }
}

function displayLocationsOnMap(locations, layerGroup, groupName) {
    layerGroup.clearLayers(); // تنظيف الطبقة قبل إضافة علامات جديدة
    locations.forEach((location) => {
        const locationLatLng = [location.latitude, location.longitude];
        const marker = L.marker(locationLatLng).addTo(layerGroup);

        // إنشاء محتوى مخصص للنافذة المنبثقة
        const popupContent = `
            <div class="custom-popup">
                <h3>${location.name}</h3>
                <p><strong>Type:</strong> ${location.field_type}</p>
                <p>${location.description}</p>
                ${location.image ? `<img src="${location.image}" alt="${location.name}" class="popup-image">` : ""}
                <p><strong>Address:</strong> ${location.address}</p>
                
                <!-- إضافة الرابط للمشاركة -->
                <a href="https://example.com?lat=${location.latitude}&lng=${location.longitude}" target="_blank" class="popup-link">Share this location with another app</a>
            </div>
        `;

        // إضافة النافذة المنبثقة المخصصة إلى العلامة
        marker.bindPopup(popupContent);
    });
}
