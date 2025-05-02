

// Initialize map
const map = L.map('flight-map').setView([51.47, -0.45], 10);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
}).addTo(map);

// Flight markers
let flightMarkers = [];

// Update flight data and map
async function fetchFlightData() {
    const response = await fetch("/flights-data");
    const data = await response.json();
    
    // Clear existing markers
    flightMarkers.forEach(marker => map.removeLayer(marker));
    flightMarkers = [];
    
    // Process inbound flights
    let inboundHTML = "<h3>Inbound Flights</h3><ul>";
    data.inbound.forEach(f => {
        inboundHTML += `<li>${f.callsign} | ${f.altitude}m | ${f.status}</li>`;
        
        // Add marker to map
        if (f.latitude && f.longitude) {
            const markerColor = f.status.includes("LANDING") ? "orange" : "green";
            const marker = L.marker([f.latitude, f.longitude])
                .addTo(map)
                .bindPopup(`<b>${f.callsign}</b><br>Altitude: ${f.altitude} m<br>Speed: ${f.speed} m/s<br>Status: ${f.status}`);
            
            marker.setIcon(L.AwesomeMarkers.icon({
                markerColor: markerColor,
                iconColor: 'white',
                icon: 'info-sign',
                prefix: 'glyphicon'
            }));
            
            flightMarkers.push(marker);
        }
    });
    inboundHTML += "</ul>";
    
    // Process outbound flights
    let outboundHTML = "<h3>Outbound Flights</h3><ul>";
    data.outbound.forEach(f => {
        outboundHTML += `<li>${f.callsign} | ${f.altitude}m | ${f.status}</li>`;
        
        // Add marker to map
        if (f.latitude && f.longitude) {
            const marker = L.marker([f.latitude, f.longitude])
                .addTo(map)
                .bindPopup(`<b>${f.callsign}</b><br>Altitude: ${f.altitude} m<br>Speed: ${f.speed} m/s<br>Status: ${f.status}`);
            
            marker.setIcon(L.AwesomeMarkers.icon({
                markerColor: 'blue',
                iconColor: 'white',
                icon: 'info-sign',
                prefix: 'glyphicon'
            }));
            
            flightMarkers.push(marker);
        }
    });
    outboundHTML += "</ul>";
    
    document.getElementById("flight-inbound").innerHTML = inboundHTML;
    document.getElementById("flight-outbound").innerHTML = outboundHTML;
}

// Update every 30 seconds
setInterval(fetchFlightData, 30000);

// Initial load
fetchFlightData();

// Resize map when window is resized
window.addEventListener('resize', function() {
    map.invalidateSize();
});