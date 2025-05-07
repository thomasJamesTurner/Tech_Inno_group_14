async function fetchWeatherData() {
    try {
        const response = await fetch("/weather-data");
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update the weather icons element
        const currentWeatherBox = document.getElementById("weather-icons");
        if (data) {
            // Display weather data
            currentWeatherBox.innerHTML = 
            `
                <div>Current Weather: ${data[0].weathercode}</div>
            `;
        } else {
            currentWeatherBox.innerHTML = "Weather data unavailable";
        }
        const forecastWeather = document.getElementById("weather-forecast")
        if(data) 
        {
            const time = [];
            const weather = [];
            //const temperature = [8];
            for(let i =0;i<8;i++)
            {
                console.log(data[i])
                const formattedTime = (data[i].time).slice(11,16);
                const temperature = data[i].temperature + "°C\n";
                const weatherType = data[i].weathercode;
                time.push(`<td>${formattedTime}</td>`);
                //temperature.push(`<td>${temperature}</td>`)
                weather.push(`<td>${weatherType}`)
            }

            forecastWeather.innerHTML = 
            `
                <div>
                    <table>
                        <tr>
                            <th colspan = "8">Daily Forecast</th>
                        </tr>
                        <tr>
                            ${time.join('')}
                        </tr>
                        <tr>
                            ${weather.join('')}
                        </tr>
                    </table>
                </div>
            `
        }
    } catch (error) {
        console.error("Error fetching weather data:", error);
        document.getElementById("weather-icons").innerHTML = "Unable to load weather data";
    }
}



setInterval(fetchWeatherData, 3000);