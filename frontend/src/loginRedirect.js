document.addEventListener("DOMContentLoaded", async () => {
        try {
            // Validate the token with a backend API call
            const response = await fetch("/api/v1/accounts/token/custom_verify/", {
                method: "POST",
                headers: { 
                    credentials: "include",    
                }
            });

            if (response.ok) {
                // If the token is valid, redirect to the main page
                window.location.href = "/";
            } else {
                // If invalid, remove the token and stay on login page
                localStorage.removeItem("ft_transcendence-app-auth");
                localStorage.removeItem("ft_transcendence-app-refresh-token");
            }
        } catch (error) {
            console.error("Token validation failed", error);
            localStorage.removeItem("ft_transcendence-app-auth");
            localStorage.removeItem("ft_transcendence-app-refresh-token");
        }
});
