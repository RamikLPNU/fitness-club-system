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

function loadDashboardStats() {
  fetch(`${API_BASE}/stats/dashboard`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("clientsCount").innerText = data.clients;
      document.getElementById("trainersCount").innerText = data.trainers;
      document.getElementById("membershipsCount").innerText = data.active_memberships;
    })
    .catch(err => console.error("Stats error:", err));
}


document.addEventListener("DOMContentLoaded", () => {
  loadClients();
  loadDashboardStats();
});
