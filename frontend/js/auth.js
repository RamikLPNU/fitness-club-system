function login() {
  if (document.getElementById("password").value === "admin124") {
    localStorage.setItem("isAdmin", "true");
    window.location.href = "/admin_dashboard";
  } else {
    alert("Невірний пароль");
  }
}