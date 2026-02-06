const API_BASE = "http://localhost:8000/api";

let trainerChart = null;

document.getElementById("loadTrainerBtn")
    .addEventListener("click", loadTrainerLoad);

function loadTrainerLoad() {
    const month = document.getElementById("month").value;
    const year = document.getElementById("year").value;

    fetch(`${API_BASE}/reports/trainer-load?month=${month}&year=${year}`)
        .then(res => res.json())
        .then(data => {
            const ctx = document
                .getElementById("adminTrainerChart")
                .getContext("2d");

            // знищуємо старий графік
            if (trainerChart) {
                trainerChart.destroy();
            }

            trainerChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.map(d => d.trainer),
                    datasets: [{
                        label: "Кількість занять",
                        data: data.map(d => d.sessions),
                        backgroundColor: "rgba(75, 192, 192, 0.7)",
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { stepSize: 1 }
                        }
                    }
                }
            });
        });
}

document.addEventListener("DOMContentLoaded", () => {
    loadTrainerLoad();
});
