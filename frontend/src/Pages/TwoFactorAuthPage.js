import VerificationButton from "../Components/VerificationButton.js";

class TwoFactorAuthPage {
    template() {
        const container = document.createElement("div");
        container.classList.add("two-factor-auth");

        const TwoFactorAuthTitle = document.createElement("h1");
        TwoFactorAuthTitle.textContent = "2FA 인증방식을 선택하세요";

        const authenticatorBtn = VerificationButton(
            "white",
            "tomato",
            "Authenticator App"
        );

        const cancelBtn = VerificationButton("black", "white", "Cancel");

        container.appendChild(TwoFactorAuthTitle);
        container.appendChild(authenticatorBtn);
        container.appendChild(cancelBtn);

        return container;
    }
}

// Instantiate the 2FA verification page
export default new TwoFactorAuthPage();
