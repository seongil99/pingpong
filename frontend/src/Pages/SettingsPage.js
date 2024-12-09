import NavBar from "../Components/Navbar";

class SettingsPage {
    template() {
        const settingsTitle = document.createElement("h1");
        const settingsList = document.createElement("ul");
        const settingsItem = ["Profile", "2FA", "Withdraw"];
        for (let item of settingsItem)
            settingsList.appendChild(createElement("li", {}, item));
        const a1 = createElement("div", {}, settingsTitle, settingsList);
        const navBar = NavBar();
        const main = createElement("main", {}, a1);
        const container = createElement("div", {}, navBar, main);
        return container;
    }
}

export default SettingsPage;
