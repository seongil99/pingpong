import createElement from "../Utils/createElement.js";
import AuthForm from "../Components/Auth/AuthForm.js";

class AuthPage {
    template(pathParam, queryParam) {
        const TwoFactorAuthTitle = createElement(
            "h1",
            {},
            i18next.t("auth_page_title")
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
