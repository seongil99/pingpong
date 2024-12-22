const verifyOTP = async (otp) => {
    try {
        const response = await fetch("/api/v1/users/accounts/mfa/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({ otp }),
        });
        const data = await response.json();
        if (!response.ok) {
            document.getElementById("error-message").textContent =
                data.error || "Verification failed. Please try again.";
            return ;
        }
        alert("2FA verification successful!");
        await window.router.navigate("/home", true);
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("error-message").textContent =
            "An error occurred. Please try again.";
    }
};

export default verifyOTP;
