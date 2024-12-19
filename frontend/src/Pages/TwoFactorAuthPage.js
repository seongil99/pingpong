import createElement from "../Utils/createElement.js";

class TwoFactorAuthPage {
    template(pathParam, queryParam) {
        const MultiFactorAuthTitle = createElement(
            "h1",
            {},
            "2FA 인증방식을 선택하세요"
        );
        const authenticatorBtn = createElement(
            "button",
            {
                class: "navigate",
                path: "/otp/auth",
                style: {
                    color: "white",
                    backgroundColor: "tomato",
                },
            },
            "Authenticator App"
        );
        const cancelBtn = createElement(
            "button",
            {
                class: "navigate",
                path: "/",
                style: {
                    color: "black",
                    backgroundColor: "white",
                },
            },
            "Cancel"
        );
        const container = createElement(
            "div",
            {
                class: "two-factor-auth",
            },
            MultiFactorAuthTitle,
            authenticatorBtn,
            cancelBtn
        );
        return container;
    }
}

// Instantiate the 2FA verification page
export default TwoFactorAuthPage;
