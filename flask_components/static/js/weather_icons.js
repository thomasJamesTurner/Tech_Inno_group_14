async function fetchWeatherData() {
    try {
        const response = await fetch("/weather-data");
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update current weather
        const currentWeatherBox = document.getElementById("weather-icons");
        if (data.current_weather) {
            currentWeatherBox.innerHTML = 
            `
                <div>Current Weather: ${data.current_weather.weather_description}</div>
                <img src="${data.current_weather.weather_image}" alt="${data.current_weather.weather_description}">
                <div>Temperature: ${data.current_weather.temperature}°C</div>
            `;
        } else {
            currentWeatherBox.innerHTML = "Weather data unavailable";
        }

        // Update forecast
        const forecastWeather = document.getElementById("weather-forecast");
        if(data.forecast && data.forecast.length > 0) {
            const time = [];
            const weather = [];
            const temp = [];
            
            data.forecast.forEach(hour => {
                const formattedTime = hour.time.slice(11,16);
                time.push(`<td>${formattedTime}</td>`);
                weather.push(`<td><img src="${hour.weather_image}" alt="${hour.weather_description}"></td>`);
                temp.push(`<td>${hour.temperature}°C</td>`);
            });

            forecastWeather.innerHTML = 
            `
                <div>
                    <table>
                        <tr>
                            <th colspan="${data.forecast.length}">Hourly Forecast</th>
                        </tr>
                        <tr>
                            ${time.join('')}
                        </tr>
                        <tr>
                            ${weather.join('')}
                        </tr>
                        <tr>
                            ${temp.join('')}
                        </tr>
                    </table>
                </div>
            `;
        }
    } catch (error) {
        console.error("Error fetching weather data:", error);
        document.getElementById("weather-icons").innerHTML = "Unable to load weather data";
        document.getElementById("weather-forecast").innerHTML = "";
    }
}

setInterval(fetchWeatherData, 3000);