const enableOTP = async (otp) => {
    try {
        const response = await fetch("/api/v1/users/accounts/mfa/", {
            method: "PUT",
            headers: {
				"Content-Type": "application/json",
            },
			credentials: "include",
            body: JSON.stringify({ otp }),
        });
        if (!response.ok) {
			throw new Error(response.json());
        }
		alert("MFA Enabled!!");
		window.location.reload();
    } catch (error) {
        console.error("Error:", error);
    }
};

export default enableOTP;
