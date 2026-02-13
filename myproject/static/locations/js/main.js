const map = L.map('map').setView([31.5, 34.5], 10);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

map.locate({ setView: true, maxZoom: 16 });

const nearbyFieldsLayer = L.layerGroup().addTo(map);
const allFieldsLayer = L.layerGroup().addTo(map);
const filteredFieldsLayer = L.layerGroup().addTo(map);

map.on('locationfound', async (e) => {
    const userLatLng = e.latlng;

    L.circle(userLatLng, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 50 
    }).addTo(map).bindPopup("Your Current Location").openPopup();

    L.marker(userLatLng).addTo(map).bindPopup("Your Current Location").openPopup();

    const nearbyFields = await fetchNearbyFields(userLatLng);
    displayLocationsOnMap(nearbyFields, nearbyFieldsLayer, "Nearby Fields");

    const allFields = await fetchAllFields();
    displayLocationsOnMap(allFields, allFieldsLayer, "All Fields");

    const fieldNames = await fetchFieldNames();
    populateFieldNameSuggestions(fieldNames);

    const fieldTypes = await fetchFieldTypes();
    populateFieldTypeFilter(fieldTypes);
});

map.on('locationerror', (e) => {
    alert("Unable to locate your position: " + e.message);
});



async function fetchNearbyFields(userLatLng) {
    const { lat, lng } = userLatLng;
    const maxDistance = 10; 

    try {
        const response = await fetch(`/locations/get_nearby_fields?latitude=${lat}&longitude=${lng}&max_distance=${maxDistance}`);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error fetching nearby fields:", error);
        return [];
    }
}

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

function populateFieldTypeFilter(types) {
    const filterSelect = document.getElementById('filter-select');
    types.forEach((type) => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        filterSelect.appendChild(option);
    });

    filterSelect.addEventListener('change', async (e) => {
        const selectedType = e.target.value;
        const filteredFields = await fetchFilteredFields(selectedType);
        displayLocationsOnMap(filteredFields, filteredFieldsLayer, "Filtered Fields");
    });
}

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
    layerGroup.clearLayers(); 
    locations.forEach((location) => {
        const locationLatLng = [location.latitude, location.longitude];
        const marker = L.marker(locationLatLng).addTo(layerGroup);

        const popupContent = `
            <div class="custom-popup">
                <h3>${location.name}</h3>
                <p><strong>Type:</strong> ${location.field_type}</p>
                <p>${location.description}</p>
                ${location.image ? `<img src="${location.image}" alt="${location.name}" class="popup-image">` : ""}
                <p><strong>Address:</strong> ${location.address}</p>
                <a href="/locations/${location.id}/" target="_blank" class="popup-link">View Details</a>
            </div>
        `;

        marker.bindPopup(popupContent);
    });
}