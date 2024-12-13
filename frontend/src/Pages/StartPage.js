import createElement from "../Utils/createElement.js";

class StartPage {
    template() {
        const transcendentTitle = createElement("h1", {}, "ft_transcendence");

        // flag = detectLoginStatus();
        let flag = 1;
        let correctPath;
        if (flag === 0) correctPath = "/home";
        else if (flag === 1) correctPath = "/login";
        else if (flag === 2) correctPath = "/otp";

        // go to Login Page or 2FA Page or Main Page
        const startButton = createElement(
            "button",
            { class: "navigate", path: correctPath },
            "Sign In"
        );
        const container = createElement(
            "div",
            { class: "start" },
            transcendentTitle,
            startButton
        );
        return container;
    }
}

export default StartPage;
