
const form = document.getElementById('loginForm');

form.addEventListener("submit", function(event){
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
}).then(response => response.json().then(data => ({
        status: response.status,
        body: data
    })))
    .then(result => {
        if (result.status === 200) {
            alert(result.body.message);
        } else {
            alert(result.body.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong");
    });
});


