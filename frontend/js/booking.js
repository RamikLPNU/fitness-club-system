document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("bookingForm");
    const statusEl = document.getElementById("bookingStatus");
    const bookingList = document.getElementById("bookingList");

    const clientInput = document.getElementById("clientName");
    const dateInput = document.getElementById("trainingDate");
    const directionSelect = document.getElementById("direction");
    const trainerSelect = document.getElementById("trainer");

    /* === ФЕЙКОВІ ТРЕНЕРИ === */
    const trainersByDirection = {
        Fitness: ["Іван Сильний", "Олег Тренер"],
        Yoga: ["Анна Спокій", "Марія Balance"],
        Crossfit: ["Дмитро Power", "Макс Steel"]
    };

    /* === ЗАВАНТАЖЕННЯ ТРЕНЕРІВ === */
    directionSelect.addEventListener("change", () => {
        const direction = directionSelect.value;
        trainerSelect.innerHTML = "<option value=''>Оберіть тренера</option>";

        if (!direction) return;

        trainersByDirection[direction].forEach(tr => {
            const option = document.createElement("option");
            option.value = tr;
            option.textContent = tr;
            trainerSelect.appendChild(option);
        });
    });

    /* === ЗАПИС НА ТРЕНУВАННЯ === */
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const booking = {
            client: clientInput.value,
            date: dateInput.value,
            direction: directionSelect.value,
            trainer: trainerSelect.value
        };

        if (!booking.client || !booking.date || !booking.direction || !booking.trainer) {
            statusEl.textContent = "❗ Заповніть усі поля";
            return;
        }

        const bookings = JSON.parse(localStorage.getItem("bookings") || "[]");
        bookings.push(booking);
        localStorage.setItem("bookings", JSON.stringify(bookings));

        statusEl.textContent = "✅ Ви успішно записані на тренування!";
        form.reset();
        renderBookings();
    });

    /* === ВІДОБРАЖЕННЯ ЗАПИСІВ === */
    function renderBookings() {
        const bookings = JSON.parse(localStorage.getItem("bookings") || "[]");
        bookingList.innerHTML = "";

        bookings.forEach(b => {
            const li = document.createElement("li");
            li.textContent =
                `${b.client} — ${b.direction} — ${b.trainer} (${b.date})`;
            bookingList.appendChild(li);
        });
    }

    renderBookings();
});
