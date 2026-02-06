const API_BASE = "http://localhost:8000/api";

let incomeChart = null;
let trainerChart = null;

document
    .getElementById("loadIncomeBtn")
    .addEventListener("click", loadIncome);

function loadIncome() {
    const year = document.getElementById("incomeYear").value;

    fetch(`${API_BASE}/reports/income?year=${year}`)
        .then(res => {
            if (!res.ok) throw new Error("API error");
            return res.json();
        })
        .then(data => renderIncomeChart(data, year))
        .catch(err => {
            console.error(err);
            alert("Помилка завантаження доходів");
        });
}

function renderIncomeChart(data, year) {
    const ctx = document
        .getElementById("adminIncomeChart")
        .getContext("2d");

    if (incomeChart) {
        incomeChart.destroy();
    }

    incomeChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: data.map(d => d.month),
            datasets: [{
                label: `Дохід за ${year} рік`,
                data: data.map(d => d.income),
                tension: 0.35,
                borderWidth: 3,
                pointRadius: 4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        font: { size: 14 }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: ctx =>
                            ctx.parsed.y.toLocaleString("uk-UA") + " грн"
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value =>
                            value.toLocaleString("uk-UA") + " грн"
                    }
                }
            }
        }
    });
}

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
    loadIncome();
    loadTrainerLoad();
});
