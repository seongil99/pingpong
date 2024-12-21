import createElement from "../Utils/createElement.js";
import AuthForm from "../Components/Auth/AuthForm.js";

class AuthPage {
    template(pathParam, queryParam) {
        const TwoFactorAuthTitle = createElement(
            "h1",
            {},
            "2FA를 등록한 Authenticator App에 접속해서 코드번호를 입력하세요"
        );
        const authForm = AuthForm();
        const container = createElement(
            "div",
            { class: "two-factor-auth" },
            TwoFactorAuthTitle,
            authForm
        );

        return container;
    }
}

// Instantiate the 2FA verification page
export default AuthPage;
