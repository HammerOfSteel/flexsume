const loginForm = document.getElementById('login-form');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const loginData = {
        username: email,
        password: password
    };

    try {
        const response = await fetch('http://localhost:8000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        if (response.ok) {
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json();
            displayErrorMessage(errorData.detail);
        }
    } catch (error) {
        console.error('Error:', error);
        displayErrorMessage('An error occurred. Please try again.');
    }
});

function displayErrorMessage(message) {
    alert(message);
}
