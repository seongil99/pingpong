// authRedirect.js
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("/api/v1/accounts/token/custom_verify/", {
            method: "POST",
            headers: { 
                credentials: "include",
            }
        });

        if (!response.ok) {
            console.error("Token validation failed", response);
            localStorage.removeItem("ft_transcendence-app-auth");
            localStorage.removeItem("ft_transcendence-app-refresh-token");
            window.location.href = "/login.html";
        }
    } catch (error) {
        console.error("Token validation failed", error);
        window.location.href = "/login.html";
    }
});
