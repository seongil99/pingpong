class TwoFactorAuthPage {
    template() {
        return this.init();
    }

    createElement() {
        // Create the HTML structure for the 2FA verification page
        const container = document.createElement('div');
        const innerHtml = `
            <h2>2FA Verification</h2>
            <p>Please enter the OTP sent to your device.</p>
            <form id="2fa-form">
                <input type="text" id="otp" placeholder="Enter OTP" required>
                <button type="submit">Verify OTP</button>
            </form>
            <div id="error-message" style="color: red; text-align: center; display: none;"></div>
        `;
        container.innerHTML = innerHtml;
        return container; // Return the HTML string
    }

    init() {
        const html = this.createElement(); // Get the HTML from template
        // Here you can use the returned HTML as needed
        // Example: this.container.innerHTML = html; // Uncomment if needed later
        this.bindEvents(); // Bind event handlers
        return html;
    }

    bindEvents() {
        // Add event listener for the form submission
        document.addEventListener('submit', (event) => {
            if (event.target.id === '2fa-form') {
                event.preventDefault();
                this.verifyOTP(); // Call the method to verify OTP
            }
        });
    }

    async verifyOTP() {
        const otp = document.getElementById('otp').value;

        try {
            const response = await fetch('/api/v1/accounts/two-factor-auth/verifications/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ otp }),
            });
            const data = await response.json();

            if (response.ok) {
                // Redirect to the main app or dashboard
                alert('2FA verification successful!');
                // window.location.href = '/';
            } else {
                this.showErrorMessage(data.error || 'Verification failed. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showErrorMessage('An error occurred. Please try again.');
        }
    }

    showErrorMessage(message) {
        const errorMessage = document.getElementById('error-message');
        errorMessage.innerText = message;
        errorMessage.style.display = 'block';
    }
}

// Instantiate the 2FA verification page
export default new TwoFactorAuthPage();
