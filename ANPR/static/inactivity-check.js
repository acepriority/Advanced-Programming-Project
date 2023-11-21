// inactivity-check.js
function keepSessionAlive() {
    // Send an AJAX request to keep the session alive
    fetch('/keep-alive/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token if using Django's CSRF protection
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error keeping session alive:', error);
    });
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize the inactivity check
function initializeInactivityCheck() {
    let lastActivityTime = Date.now();
    let timeoutId;

    // Set the inactivity check interval (e.g., every minute)
    const inactivityCheckInterval = 60 * 1000;  // 60 seconds

    function showConfirmationMessage() {
        const confirmationMessage = document.createElement('div');
        confirmationMessage.innerHTML = `
            <div id="confirmation-message" style="position: fixed; top: 30%; left: 50%; transform: translate(-50%, -50%); background-color: #f0f0f0; padding: 20px; border: 1px solid #ccc; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); text-align: center;">
                <p style="margin-bottom: 10px; font-size: 16px;">Are you still there? Your session will expire soon, Do you want to extend?.</p>
                <button onclick="confirmSession()" style="padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; margin-right: 10px;">Yes</button>
                <button onclick="logoutAndClose()" style="padding: 10px 20px; background-color: #FF4D4D; color: white; border: none; border-radius: 5px; cursor: pointer;">No</button>
            </div>
        `;
        document.body.appendChild(confirmationMessage);

        // Set a timer to remove the confirmation message after 10 seconds
        timeoutId = setTimeout(() => {
            confirmationMessage.remove();
            logoutAndClose();
        }, 10000);
    }

    function handleUserActivity() {
        const currentTime = Date.now();
        const timeSinceLastActivity = currentTime - lastActivityTime;

        // If enough time has passed, show the confirmation message
        if (timeSinceLastActivity >= inactivityCheckInterval) {
            showConfirmationMessage();
        } else {
            // Reset the timer
            clearTimeout(timeoutId);
            // Restart the inactivity check timer
            timeoutId = setTimeout(showConfirmationMessage, inactivityCheckInterval - timeSinceLastActivity);
        }

        lastActivityTime = currentTime;
        keepSessionAlive();  // Keep the session alive when user is active
    }

    window.confirmSession = function () {
        // User wants to keep the session active
        clearTimeout(timeoutId);
        const confirmationMessage = document.getElementById('confirmation-message');
        if (confirmationMessage) {
            confirmationMessage.remove();
        }
        keepSessionAlive();
    };

    window.logoutAndClose = function () {
        // User wants to log out
        const confirmationMessage = document.getElementById('confirmation-message');
        if (confirmationMessage) {
            confirmationMessage.remove();
        }
        window.location.href = '/logout/';
    };

    // Add event listeners for user activity
    document.addEventListener('mousemove', handleUserActivity);
    document.addEventListener('keydown', handleUserActivity);

    // Set interval for showing the confirmation message
    setInterval(handleUserActivity, inactivityCheckInterval);
}

// Start the inactivity check when the page loads
document.addEventListener('DOMContentLoaded', initializeInactivityCheck);
