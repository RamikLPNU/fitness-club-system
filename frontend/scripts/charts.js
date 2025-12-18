const API_BASE = "http://localhost:8000"; // твій FastAPI сервер

// --- 1. Активність клієнтів ---
fetch(`${API_BASE}/api/reports/client-activity`)
  .then(res => res.json())
  .then(data => {
    const ctx = document.getElementById("clientActivityChart").getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: data.map(d => d.client),
        datasets: [{
          label: "Кількість відвідувань",
          data: data.map(d => d.visits),
          backgroundColor: "rgba(75, 192, 192, 0.6)"
        }]
      },
      options: { responsive: true }
    });
  });

// --- 2. Доходи клубу ---
fetch(`${API_BASE}/api/reports/income?year=2025`)
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

// --- 3. Завантаженість тренерів ---
fetch(`${API_BASE}/api/reports/trainer-load`)
  .then(res => res.json())
  .then(data => {
    const ctx = document.getElementById("trainerLoadChart").getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: data.map(d => `${d.trainer} (${d.hall})`),
        datasets: [{
          label: "Кількість занять",
          data: data.map(d => d.sessions),
          backgroundColor: "rgba(255, 159, 64, 0.6)"
        }]
      },
      options: { responsive: true }
    });
  });
