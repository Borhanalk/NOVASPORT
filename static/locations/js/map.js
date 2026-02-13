document.addEventListener("DOMContentLoaded", function () {
    // 1. إنشاء الخريطة بدون مركز افتراضي
    var map = L.map('map');

    // 2. إضافة الطبقة الأساسية للخريطة
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // 3. جلب البيانات من العنصر المخفي في HTML
    var fields = JSON.parse(document.getElementById('fields-data').textContent);

    // 4. إضافة النقاط (Markers) إلى الخريطة
    var bounds = [];
    fields.forEach(function (field) {
        var marker = L.marker([field.latitude, field.longitude]).addTo(map);
        marker.bindPopup(`
            <b>${field.name}</b><br>
            Type: ${field.type}<br>
            Address: ${field.address}
        `);
        bounds.push([field.latitude, field.longitude]);
    });

    // 5. محاولة تحديد موقع المستخدم
    map.locate({ setView: true, maxZoom: 16 }); // تكبير الخريطة عند العثور على الموقع

    // 6. عند العثور على موقع المستخدم
    map.on('locationfound', function (e) {
        var radius = e.accuracy;

        // إضافة علامة تمثل الموقع الحالي
        L.marker(e.latlng).addTo(map)
            .bindPopup("You are here! Accuracy: " + radius.toFixed(2) + " meters.")
            .openPopup();

        // إضافة دائرة تمثل دقة الموقع
        L.circle(e.latlng, radius).addTo(map);
    });

    // 7. في حالة عدم القدرة على تحديد الموقع
    map.on('locationerror', function () {
        alert("Unable to find your location. Please enable location access.");
    });

    // 8. ضبط الخريطة لتشمل جميع النقاط إذا لم يتم العثور على الموقع
    if (bounds.length > 0) {
        map.fitBounds(bounds); // ملاءمة الخريطة لجميع النقاط
    } else {
        map.setView([31.5, 34.4667], 14); // مركز افتراضي إذا لم يتم تمرير بيانات
    }
});
