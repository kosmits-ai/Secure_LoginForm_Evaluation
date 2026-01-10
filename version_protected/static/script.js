// --------------------
// LOGIN FORM (index.html)
// --------------------
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    })
    .then(response => response.json().then(data => ({
      status: response.status,
      body: data
    })))
    .then(result => alert(result.body.message))
    .catch(error => {
      console.error("Error:", error);
      alert("Something went wrong");
    });
  });
}



