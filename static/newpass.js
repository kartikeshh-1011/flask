document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Stop page refresh

    const newPassword = document.getElementById("username").value.trim();
    const confirmPassword = document.getElementById("password").value.trim();

    // Check empty fields
    if (newPassword === "" || confirmPassword === "") {
        alert("Please fill in both password fields");
        return;
    }

    // Password length validation
    if (newPassword.length < 6) {
        alert("Password must be at least 6 characters long");
        return;
    }

    // Match passwordsfio
    if (newPassword !== confirmPassword) {
        alert("Passwords do not match");
        return;
    }

    // Success
    alert("Password changed successfully!");

    // Redirect to login page
    window.location.href = "login.html";
});

