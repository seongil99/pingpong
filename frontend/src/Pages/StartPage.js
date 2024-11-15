class StartPage {
    template() {
        const container = document.createElement("div");
        container.classList.add("start");

        const transcendentTitle = document.createElement("h1");
        transcendentTitle.textContent = "ft_transcendence";

        // go to Login Page or 2FA Page or Main Page
        const startButton = document.createElement("button");
        // flag = detectLoginStatus();
        let flag = 1;
        let correctPath;
        if (flag === 0) correctPath = "/home";
        else if (flag === 1) correctPath = "/login";
        else if (flag === 2) correctPath = "/verification";

        startButton.classList.add("navigate");
        startButton.setAttribute("path", correctPath);
        startButton.textContent = "시작하기";

        container.appendChild(transcendentTitle);
        container.appendChild(startButton);

        return container;
    }
}

export default new StartPage();