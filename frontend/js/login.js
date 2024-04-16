// Get the login form element
const loginForm = document.getElementById('login-form');

// Add event listener to the login form submission
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent the default form submission

    // Get the email and password values from the form
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Create an object with the login credentials
    const loginData = {
        email: email,
        password: password
    };

    try {
        // Make a POST request to the login API endpoint
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        if (response.ok) {
            // Login successful, redirect to the dashboard page
            window.location.href = 'index.html';
        } else {
            // Login failed, display an error message
            const errorData = await response.json();
            displayErrorMessage(errorData.message);
        }
    } catch (error) {
        console.error('Error:', error);
        displayErrorMessage('An error occurred. Please try again.');
    }
});

// Function to display an error message
function displayErrorMessage(message) {
    const errorElement = document.createElement('p');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    loginForm.appendChild(errorElement);
}