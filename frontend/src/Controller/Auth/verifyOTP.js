const verifyOTP = async (otp) => {
    try {
        const response = await fetch("/api/v1/users/accounts/mfa/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ otp }),
        });
        const data = await response.json();

        if (response.ok) {
            // Redirect to the main app or dashboard
            alert("2FA verification successful!");
            window.location.href = "/home";
            // location.reload();
        } else {
            document.getElementById("error-message").textContent =
                data.error || "Verification failed. Please try again.";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("error-message").textContent =
            "An error occurred. Please try again.";
    }
};

export default verifyOTP;
