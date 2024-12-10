import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";

class SettingsPage {
    async template() {
        const title1 = createElement("h1", {class: "settings-section-title"}, "Edit Profile");
		const title2 = createElement("h1", {class: "settings-section-title"}, "2FA Enable/Disable");
		const title3 = createElement("h1", {class: "settings-section-title"}, "Inactive Account");
		const editProfileForm = ProfileForm();
        const twoAuthBtn = createElement("button", {class: "settings-btn", events: {click: }}, );
        const editProfileSection = createElement(
            "section",
            { class: "settings-section" },
            title1,
            editProfileForm
        );
        const twoAuthSection = createElement(
            "section",
            { class: "settings-section" },
            title2,
            twoAuthBtn
        );
        const inactivateAccountSection = createElement(
            "section",
            { class: "settings-section" },
            title3,
            inactiveBtn
        );
        const modal = SettingsModal();
        const navBar = NavBar();
        const main = createElement(
            "main",
            { class: "settings-content" },
            editProfileSection,
            twoAuthSection,
            inactivateAccountSection
        );
        const container = createElement("div", {}, modal, navBar, main);
        return container;
    }
}

export default SettingsPage;