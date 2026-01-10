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

// --------------------
// STATUS FORM (dashboard.html)
// --------------------
const statusForm = document.getElementById("statusForm");
if (statusForm) {
  const input = document.getElementById("statusInput");
  const preview = document.getElementById("statusPreview");

  statusForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const status = input.value;

    //  VULNERABLE (Version 4)
    preview.innerHTML = status; //user iunput is directly injected into HTML. Malicious users can exploit this vulnerability and change the structure of the page or execute harmful scripts.

    // Secure version would be:
    // preview.textContent = status; // This treats user input as plain text, preventing HTML interpretation.

    
  });
}


