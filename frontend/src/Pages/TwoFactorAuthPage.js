import createElement from "../Utils/createElement.js";

// createElement() {
//     // Create the HTML structure for the 2FA verification page
//     const container = document.createElement("div");
//     const innerHtml = `
//             <h2>2FA Verification</h2>
//             <p>Please enter the OTP sent to your device.</p>
//             <form id="2fa-form">
//                 <input type="text" id="otp" placeholder="Enter OTP" required>
//                 <button type="submit">Verify OTP</button>
//             </form>
//             <div id="error-message" style="color: red; text-align: center; display: none;"></div>
//         `;
//     container.innerHTML = innerHtml;
//     return container; // Return the HTML string
//   }

class TwoFactorAuthPage {
    template() {
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
