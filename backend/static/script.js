// AQI Prediction Frontend Script

document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('aqiForm');
    const loading = document.getElementById('loading');
    const resultContent = document.getElementById('resultContent');

    const aqiValue = document.getElementById('aqiValue');
    const categoryName = document.getElementById('categoryName');
    const categoryDescription = document.getElementById('categoryDescription');
    const aqiCategory = document.getElementById('aqiCategory');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const pollutantData = {
            PM25: parseFloat(document.getElementById('pm25').value),
            PM10: parseFloat(document.getElementById('pm10').value),
            NO2: parseFloat(document.getElementById('no2').value),
            SO2: parseFloat(document.getElementById('so2').value),
            CO: parseFloat(document.getElementById('co').value),
            O3: parseFloat(document.getElementById('o3').value)
        };

        loading.style.display = 'block';
        resultContent.style.display = 'none';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(pollutantData)
            });

            if (!response.ok) throw new Error("Prediction failed");

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            alert("Error: " + error.message);
            loading.style.display = 'none';
            resultContent.style.display = 'block';
        }
    });

    function displayResults(data) {
        loading.style.display = 'none';
        resultContent.style.display = 'block';

        aqiValue.textContent = data.aqi;
        aqiValue.style.color = data.color;

        categoryName.textContent = data.category;
        categoryDescription.textContent = data.description;
        aqiCategory.style.borderLeftColor = data.color;

        aqiValue.classList.add('fade-in');
        setTimeout(() => aqiValue.classList.remove('fade-in'), 500);
    }
});
