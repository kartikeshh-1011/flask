document.addEventListener('DOMContentLoaded', function () {
    // Select all flash messages
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function (msg) {
        // Add close functionality if close button exists
        const closeBtn = msg.querySelector('.close-flash');
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                msg.classList.add('fade-out');
                setTimeout(() => msg.remove(), 300);
            });
        }

        // Auto-hide after 5 seconds
        setTimeout(function () {
            if (msg.parentElement) { // Check if it hasn't been removed manually
                msg.classList.add('fade-out');
                setTimeout(() => msg.remove(), 300);
            }
        }, 5000);
    });
});
