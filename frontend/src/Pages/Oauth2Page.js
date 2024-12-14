import detectMfaEnabled from "../Controller/Auth/detectMfaEnabled.js"

class Oauth2Page {
    async template() {
        // 컨테이너 div 생성
        try {
            const callBackUri =
                "https://localhost/api/v1/users/accounts/oauth2/fortytwo/login/callback/";
            const queryParam = new URLSearchParams(window.location.search);
            const code = queryParam.get("code");
            // const csrftoken = document.cookie
            //     .split("; ")
            //     .find((row) => row.startsWith("csrftoken="))
            //     .split("=")[1];
            const response = await fetch(callBackUri, {
                method: "POST",
                redirect: "manual",
                headers: {
                    "Content-Type": "application/json",
                    // "X-CSRFToken": csrftoken,
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
            console.log(error);
        }
        const container = document.createElement("div");

        return container; // 최종 DOM을 반환
    }
}

export default Oauth2Page;
