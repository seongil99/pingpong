import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import handleEmailLogin from "../Controller/Auth/handleEmailLogin.js";

class LoginPage {
    template() {
        const title = createElement("h2", {}, "Login Page");
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
                            "u-s4t2ud-80c35252b5c6defa03f294f295f7bc83623a37a929b5ade66bed0dbafce4f667";
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
            {},
            title,
            loginBtn,
            fortytwoLoginBtn
        );

        return container; // 최종 DOM 반환
    }
}

export default LoginPage;
