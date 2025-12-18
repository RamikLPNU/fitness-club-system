const API_BASE = "http://localhost:8000/api";


function loadClients() {
  fetch(`${API_BASE}/clients`)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector("#clientsTable tbody");
      tbody.innerHTML = "";
      data.forEach(c => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${c.full_name}</td>
          <td>${c.age}</td>
          <td>${c.phone}</td>
          <td>${c.email}</td>
          <td>
            <button onclick="deleteClient(${c.client_id})">Видалити</button>
          </td>`;
        tbody.appendChild(tr);
      });
    });
}

document.getElementById("clientForm").addEventListener("submit", e => {
  e.preventDefault();
  const client = {
    full_name: document.getElementById("fullName").value,
    age: document.getElementById("age").value,
    phone: document.getElementById("phone").value,
    email: document.getElementById("email").value
  };
  fetch(`${API_BASE}/clients`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(client)
  }).then(() => loadClients());
});

function deleteClient(id) {
  fetch(`${API_BASE}/clients/${id}`, { method: "DELETE" })
    .then(() => loadClients());
}


function loadTrainers() {
  fetch(`${API_BASE}/trainers`)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector("#trainersTable tbody");
      tbody.innerHTML = "";
      data.forEach(t => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${t.full_name}</td>
          <td>${t.specialization}</td>
          <td>${t.phone}</td>
          <td>
            <button onclick="deleteTrainer(${t.trainer_id})">Видалити</button>
          </td>`;
        tbody.appendChild(tr);
      });
    });
}

document.getElementById("visitForm").addEventListener("submit", e => {
  e.preventDefault();

  const params = new URLSearchParams({
    client_id: document.getElementById("visitClientId").value,
    trainer_id: document.getElementById("visitTrainerId").value,
    class_id: document.getElementById("visitClassId").value,
    date_id: document.getElementById("visitDateId").value
  });

  fetch(`${API_BASE}/visits?${params.toString()}`, {
    method: "POST"
  })
  .then(res => res.json())
  .then(data => alert(data.message));
});


document.getElementById("trainerForm").addEventListener("submit", e => {
  e.preventDefault();
  const trainer = {
    full_name: document.getElementById("trainerName").value,
    specialization: document.getElementById("specialization").value,
    phone: document.getElementById("trainerPhone").value
  };
  fetch(`${API_BASE}/trainers`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(trainer)
  }).then(() => loadTrainers());
});

function deleteTrainer(id) {
  fetch(`${API_BASE}/trainers/${id}`, { method: "DELETE" })
    .then(() => loadTrainers());
}


function loadMemberships() {
  fetch(`${API_BASE}/memberships`)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector("#membershipsTable tbody");
      tbody.innerHTML = "";
      data.forEach(m => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${m.name}</td>
          <td>${m.duration_days}</td>
          <td>${m.price}</td>
          <td>
            <button onclick="deleteMembership(${m.membership_id})">Видалити</button>
          </td>`;
        tbody.appendChild(tr);
      });
    });
}

function loadTrainerProfile() {
  const id = document.getElementById("trainerProfileId").value;

  fetch(`${API_BASE}/trainers/${id}/profile`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("trainerInfo").innerHTML = `
        <b>${data.trainer.full_name}</b><br>
        Спеціалізація: ${data.trainer.specialization}<br>
        Телефон: ${data.trainer.phone}
      `;

        Object.entries(data.schedule).forEach(([day, time]) => {
        document.getElementById("schedule").innerHTML +=
            `<li><strong>${day}:</strong> ${time}</li>`;
        });
        
      const tbody = document.getElementById("trainerSessions");
      tbody.innerHTML = "";
      data.sessions.forEach(s => {
        tbody.innerHTML += `
          <tr>
            <td>${s.date_id}</td>
            <td>${s.client_name}</td>
            <td>${s.class_name}</td>
          </tr>`;
      });
    });
}


document.getElementById("membershipForm").addEventListener("submit", e => {
  e.preventDefault();
  const membership = {
    name: document.getElementById("membershipName").value,
    duration_days: document.getElementById("duration").value,
    price: document.getElementById("price").value
  };
  fetch(`${API_BASE}/memberships`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(membership)
  }).then(() => loadMemberships());
});

function deleteMembership(id) {
  fetch(`${API_BASE}/memberships/${id}`, { method: "DELETE" })
    .then(() => loadMemberships());
}


function loadIncome() {
  const year = document.getElementById("incomeYear").value;
  fetch(`${API_BASE}/reports/income?year=${year}`)
    .then(res => res.json())
    .then(data => {
      const ctx = document.getElementById("adminIncomeChart").getContext("2d");
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

function loadTrainerLoad() {
  const month = document.getElementById("month").value;
  const year = document.getElementById("year").value;
  fetch(`${API_BASE}/reports/trainer-load?month=${month}&year=${year}`)
    .then(res => res.json())
    .then(data => {
      const ctx = document.getElementById("adminTrainerChart").getContext("2d");
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


document.addEventListener("DOMContentLoaded", () => {
  loadClients();
  loadTrainers();
  loadMemberships();
});
