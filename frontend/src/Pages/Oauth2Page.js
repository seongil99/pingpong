import detectMfaEnabled from "../Controller/Auth/detectMfaEnabled.js";

class Oauth2Page {
    async template() {
        try {
            const callBackUri =
                "https://localhost/api/v1/users/accounts/oauth2/fortytwo/login/callback/";
            const queryParam = new URLSearchParams(window.location.search);
            const code = queryParam.get("code");
            const response = await fetch(callBackUri, {
                method: "POST",
                redirect: "manual",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ code }),
            });
            const data = await response.json();
            if (response.ok) {
                const mfa = await detectMfaEnabled();
                if (mfa === null) {
                    alert("API Request error");
                    window.router.navigate("/login");
                }
                mfa.status === "enabled"
                    ? window.router.navigate("/otp")
                    : window.router.navigate("/home");
            } else if (data.status === "redirect") {
                window.router.navigate(data.url);
            } else {
                alert("Failed to login");
                window.router.navigate("/login");
            }
        } catch (error) {
            console.error(error);
        }
        const container = document.createElement("div");

        return container;
    }
}

export default Oauth2Page;
