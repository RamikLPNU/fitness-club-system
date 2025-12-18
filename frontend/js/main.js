const API_BASE = "http://localhost:8000/api";


function loadClients() {
  fetch(`${API_BASE}/clients`)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector("#clientsTable tbody");
      tbody.innerHTML = "";
      data.forEach(c => {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${c.full_name}</td><td>${c.age}</td><td>${c.phone}</td><td>${c.email}</td><td>${c.visit_count || 0}</td>`;
        tbody.appendChild(tr);
      });
    });
}

// Графік доходів
function loadIncome() {
  const year = document.getElementById("incomeYear").value;
  fetch(`${API_BASE}/reports/income?year=${year}`)
    .then(res => res.json())
    .then(data => {
      const ctx = document.getElementById("incomeChart").getContext("2d");
      new Chart(ctx, {
        type: "line",
        data: {
          labels: data.map(d => d.month),
          datasets: [{
            label: "Дохід (грн)",
            data: data.map(d => d.income),
            borderColor: "rgba(54, 162, 235, 1)",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            fill: true
          }]
        },
        options: { responsive: true }
      });
    });
}

// Графік завантаженості тренерів
function loadTrainerLoad() {
  const month = document.getElementById("month").value;
  const year = document.getElementById("year").value;
  fetch(`${API_BASE}/reports/trainer-load?month=${month}&year=${year}`)
    .then(res => res.json())
    .then(data => {
      const ctx = document.getElementById("trainerChart").getContext("2d");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels: data.map(d => d.trainer),
          datasets: [{
            label: "Кількість занять",
            data: data.map(d => d.sessions),
            backgroundColor: "rgba(75, 192, 192, 0.7)"
          }]
        },
        options: { responsive: true }
      });
    });
}

// Завантаження при відкритті сторінки
document.addEventListener("DOMContentLoaded", () => {
  if(document.querySelector("#clientsTable")) loadClients();
});
