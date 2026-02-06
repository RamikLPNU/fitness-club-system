const API_BASE = "http://localhost:8000/api";

const trainerList = document.getElementById("trainerList");

// набір рандомних фото
function randomTrainerPhoto() {
    const id = Math.floor(Math.random() * 1000);
    return `https://picsum.photos/400/300?random=${id}`;
}

function loadTrainers() {
    fetch(`${API_BASE}/trainers`)
        .then(res => res.json())
        .then(data => {
            trainerList.innerHTML = "";

            data.forEach(t => {
                const li = document.createElement("li");
                li.className = "trainer-card";

                li.innerHTML = `
                    <img src="${randomTrainerPhoto()}" alt="Тренер">
                    <div class="trainer-info">
                        <h3>${t.full_name}</h3>
                        <p><strong>Вік:</strong> ${t.age ?? "—"} років</p>
                        <p><strong>Спеціалізація:</strong> ${t.specialization ?? "—"}</p>
                        <p><strong>Телефон:</strong> ${t.phone ?? "—"}</p>
                    </div>
                `;

                trainerList.appendChild(li);
            });
        })
        .catch(err => {
            trainerList.innerHTML = "<p>Помилка завантаження тренерів</p>";
            console.error(err);
        });
}

document.addEventListener("DOMContentLoaded", loadTrainers);
