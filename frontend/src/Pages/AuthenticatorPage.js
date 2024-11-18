import AuthenticatorForm from "../Components/AuthenticatorForm.js";

class AuthenticatorPage {
    template() {
        const container = document.createElement("div");
        container.classList.add("two-factor-auth");

        const TwoFactorAuthTitle = document.createElement("h1");
        TwoFactorAuthTitle.textContent =
            "2FA를 등록한 Authenticator App에 접속해서 코드번호를 입력하세요";

        const authForm = new AuthenticatorForm();
        const authFormComponent = authForm.create();

        container.appendChild(TwoFactorAuthTitle);
        container.appendChild(authFormComponent);

        return container;
    }
}

// Instantiate the 2FA verification page
export default new AuthenticatorPage();
