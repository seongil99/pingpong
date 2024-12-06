import VerificationButton from "../Components/VerificationButton.js";

class MFAPage {
    template() {
        const container = document.createElement("div");
        container.classList.add("two-factor-auth");

        const MultiFactorAuthTitle = document.createElement("h1");
        MultiFactorAuthTitle.textContent = "2FA 인증방식을 선택하세요";

        const authenticatorBtn = VerificationButton(
            "white",
            "tomato",
            "Authenticator App"
        );
        authenticatorBtn.classList.add("navigate");
        authenticatorBtn.setAttribute("path", "/verification/auth");

        const cancelBtn = VerificationButton("black", "white", "Cancel");
        cancelBtn.classList.add("navigate");
        cancelBtn.setAttribute("path", "/");

        container.appendChild(MultiFactorAuthTitle);
        container.appendChild(authenticatorBtn);
        container.appendChild(cancelBtn);

        return container;
    }
}

// Instantiate the 2FA verification page
export default MFAPage;
