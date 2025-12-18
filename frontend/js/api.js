const API_URL = "http://localhost:8000";

async function apiGet(endpoint) {
  const res = await fetch(`${API_URL}${endpoint}`);
  return res.json();
}

async function apiPost(endpoint, data) {
  const res = await fetch(`${API_URL}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}
