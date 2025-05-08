async function fetchWeatherData() {
    try {
        const response = await fetch("/weather-data");
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update the weather icons element
        const weatherElement = document.getElementById("weather-icons");
        if (data) {
            // Display weather data
            weatherElement.innerHTML = 
            `
                <div>Current Weather: ${data[0]}</div>
            `;
        } else {
            weatherElement.innerHTML = "Weather data unavailable";
        }
    } catch (error) {
        console.error("Error fetching weather data:", error);
        document.getElementById("weather-icons").innerHTML = "Unable to load weather data";
    }
}



setInterval(fetchWeatherData, 3000);