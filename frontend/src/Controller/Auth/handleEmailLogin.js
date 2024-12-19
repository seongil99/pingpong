// import { getCSRFToken } from "../Utils/csrf";

const handleEmailLogin = async () => {
    // const csrfToken = getCSRFToken();
    // console.log("CSRF Token:", csrfToken);
    const url = "api/v1/users/accounts/login/"; // 로그인 API 서버 URL

    // POST 요청을 통해 서버에 로그인 요청을 보냄
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                // 'X-CSRFToken': csrfToken,
            },
            credentials: "include",
            body: JSON.stringify({
                "username": "test",
                "email": "test@example.com",
                "password": "wert2345"
            }),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        // updateNavBarLogin();
        console.dir(response);
        console.dir(data);
        if (data.is_2fa_required) {
            window.location.href = "/otp"; // 2FA 활성화 시 2FA 페이지로 이동
            return;
        }
        window.location.href = "/home"; // 로그인 성공 시 홈
    } catch (error) {
        console.error("Login failed:", error);
        alert("Login failed!");
    }
};

export default handleEmailLogin;