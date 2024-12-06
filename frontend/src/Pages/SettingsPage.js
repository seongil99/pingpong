import NavBar from "../Components/Navbar";

function item(classname, content) {
    const li = document.createElement("li");
    li.classList.add(classname);
    li.textContent = content;
    return li;
}

class StartPage {
    template() {
        const container = document.createElement("div");

        const navBar = NavBar();
        const main = document.createElement("main");
        const a1 = document.createElement("div");
        const settingsTitle = document.createElement("h1");
        const settingsList = document.createElement("ul");
        settingsList.appendChild(item("settings-item", "profile"));
        settingsList.appendChild(item("settings-item", "2FA"));
        settingsList.appendChild(item("settings-item", "Withdraw"));

        a1.appendChild(settingsTitle);
        a1.appendChild(settingsList);

        main.appendChild(a1);

        container.appendChild(navBar);
        container.appendChild(main);
        return container;
    }
}

export default StartPage;
