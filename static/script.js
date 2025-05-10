// 1. Διαχείριση Slider
document.getElementById("scenarioSlider").addEventListener("input", function() {
    const scenarioNum = this.value;
    const scenarioCode = scenarioNum.toString(2).padStart(5, '0'); // Δυαδικός κωδικός
    
    // 2. Fetch δεδομένων από Flask API
   fetch(`/api/scenario/${scenarioCode}`)
        .then(response => response.json())
        .then(data => {
            // 3. Ενημέρωση πίνακα
            updateParamsTable(data.params);
            
            // 4. Ενημέρωση γραφημάτων
            updateCharts(data.energy_data, data.cost_data);
        });
});

// 5. Επισήμανση επιλογών στον πίνακα
function updateParamsTable(params) {
    const table = document.getElementById("paramsTable");
    // ... (γεμίζει τον πίνακα και κάνει highlight τις τρέχουσες επιλογές)
}

// 6. Αρχικοποίηση γραφημάτων
const energyChart = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: ['Θέρμανση', 'Ψύξη', 'Συνολική Κατανάλωση'],
        datasets: [{
            label: 'kWh',
            data: [], // Θα ενημερώνεται δυναμικά
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
        }]
    }
});

// 7. Συνάρτηση ενημέρωσης
function updateCharts(energyData, costData) {
    energyChart.data.datasets[0].data = [
        energyData.Heating, 
        energyData.Cooling, 
        energyData.Total
    ];
    energyChart.update();
}