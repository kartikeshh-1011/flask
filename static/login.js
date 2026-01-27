// Login form - no JavaScript interference
// Form submits directly to Flask backend
let currentRole = "Student";

function setRole(role) {
    currentRole = role;
    document.getElementById("roleTitle").innerText = role + " Login";
}

console.log('Login page loaded - form will submit to backend');
