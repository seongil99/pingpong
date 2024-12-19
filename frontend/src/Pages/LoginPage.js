import createElement from "../Utils/createElement.js";
import handleEmailLogin from "../Controller/Auth/handleEmailLogin.js";

class LoginPage {
    async template(pathParam, queryParam) {
        // 제목 추가
        const title = createElement("h2", {}, "Login Page");

        // 로그인 버튼 생성
        const loginBtn = createElement(
            "button",
            {
                events: {
                    click: handleEmailLogin,
                },
            },
            "E-mail Log In"
        );

        const fortytwoLoginBtn = createElement(
            "button",
            {
                events: {
                    click: async () => {
                        const clientId =
                            "u-s4t2ud-f3c794a53848db3b102519cb5cd7123e14dae487ccdb02741f5ef3b8781504ef";
                        const redirectUri =
                            "https%3A%2F%2Flocalhost%2Foauth2%2Fredirect";
                        window.location.href = `https://api.intra.42.fr/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code`;
                    },
                },
            },
            "42 Login"
        );

        const container = createElement(
            "div",
            { class: "login-container" },
            title,
            loginBtn,
            fortytwoLoginBtn
        );

        return container; // 최종 DOM 반환
    }
}

export default LoginPage;
