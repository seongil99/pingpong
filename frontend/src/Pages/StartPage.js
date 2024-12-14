import createElement from "../Utils/createElement.js";

class StartPage {
    async template() {
        const transcendentTitle = createElement("h1", {}, "ft_transcendence");

        // go to Login Page or 2FA Page or Main Page
        const startButton = createElement(
            "button",
            { class: "navigate", path: "/login" },
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
