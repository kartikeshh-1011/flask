document.getElementById("resultForm").addEventListener("submit", function(e) {
    e.preventDefault();

    let roll = document.getElementById("roll").value;
    let dob = document.getElementById("dob").value;
    let className = document.getElementById("class").value;

    let resultBox = document.getElementById("resultBox");

    // Dummy data check
    if (roll === "101" && className === "10") {
        resultBox.style.color = "green";
        resultBox.innerHTML = `
            Name: Rahul Kumar <br>
            Class: 10th <br>
            Result: PASS <br>
            Marks: 82%
        `;
    } else {
        resultBox.style.color = "red";
        resultBox.innerHTML = "Result not found ❌";
    }
});