async function loadClients() {
  const clients = await apiGet("/clients");
  const list = document.getElementById("clients");
  list.innerHTML = "";

  clients.forEach(c => {
    const li = document.createElement("li");
    li.textContent = `${c.full_name} (${c.age} років)`;
    list.appendChild(li);
  });
}

loadClients();
