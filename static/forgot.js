document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");
    const newPasswordBtn = document.querySelector(".btn");

    newPasswordBtn.addEventListener("click", function (event) {
        event.preventDefault(); // Stop direct navigation

        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("password").value.trim();

        // Check empty fields
        if (username === "" || email === "") {
            alert("Please fill in all fields");
            return;
        }

        // Email format validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert("Please enter a valid email address");
            return;
        }

        // Success
        alert("Verification successful!");

        // Redirect after validation
        window.location.href = "newpassword.html";
    });
});

