document.getElementById("resultForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    let name = document.getElementById("name").value;
    let email = document.getElementById("Email").value;
    let className = document.getElementById("class").value;

    let resultBox = document.getElementById("resultBox");
    resultBox.innerHTML = "Loading...";
    resultBox.style.color = "#667eea";

    try {
        // Fetch result from backend API
        const response = await fetch('/get-result', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                email: email,
                class: className
            })
        });

        const data = await response.json();

        if (data.success) {
            // Display result
            resultBox.style.color = "green";
            let resultHTML = `
                <h3>✅ Result Found!</h3>
                <div style="margin-top: 20px;">
                    <p><strong>Name:</strong> ${data.student_name}</p>
                    <p><strong>Class:</strong> ${data.class}</p>
                    <p><strong>Grade:</strong> <span style="font-size: 1.5em; color: #667eea;">${data.grade}</span></p>
                    <p><strong>Percentage:</strong> ${data.percentage.toFixed(2)}%</p>
                    <p><strong>Total Marks:</strong> ${data.total_marks.toFixed(2)}</p>
                    <hr style="margin: 20px 0;">
                    <h4>Subject-wise Marks:</h4>
                    <table style="width: 100%; margin-top: 10px; border-collapse: collapse;">
                        <thead>
                            <tr style="background: #667eea; color: white;">
                                <th style="padding: 10px; text-align: left;">Subject</th>
                                <th style="padding: 10px; text-align: right;">Marks</th>
                            </tr>
                        </thead>
                        <tbody>
            `;

            for (const [subject, marks] of Object.entries(data.subjects)) {
                resultHTML += `
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="padding: 10px;">${subject}</td>
                        <td style="padding: 10px; text-align: right; font-weight: bold;">${marks}</td>
                    </tr>
                `;
            }

            resultHTML += `
                        </tbody>
                    </table>
                </div>
            `;
            resultBox.innerHTML = resultHTML;
        } else {
            resultBox.style.color = "red";
            resultBox.innerHTML = `❌ ${data.message}`;
        }
    } catch (error) {
        resultBox.style.color = "red";
        resultBox.innerHTML = "❌ Error fetching result. Please try again.";
        console.error('Error:', error);
    }
});