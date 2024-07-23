async function getWeather() {
    const city=document.getElementById('cityInput').value;
    const apiKey='ee93cd962bca4c249f7152750240307'; 
    const url=`http://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${city}&days=7`;

    try {
        const response=await fetch(url);
        const data=await response.json();

        if (response.ok) {
            const weatherResult=`
                <h2>${data.location.name}, ${data.location.country}</h2>
                <p>Temperature: ${data.current.temp_c}°C</p>
                <p>Weather: ${data.current.condition.text}</p>
                <p>Humidity: ${data.current.humidity}%</p>
                <p>Wind Speed: ${data.current.wind_kph} kph</p>`;
            document.getElementById('weatherResult').innerHTML=weatherResult;
        } else {
            document.getElementById('weatherResult').innerHTML=`<p>${data.error.message}</p>`;
        }
    } catch (error) {
        document.getElementById('weatherResult').innerHTML=`<p>Error fetching weather data. Please try again later.</p>`;
    }
}
