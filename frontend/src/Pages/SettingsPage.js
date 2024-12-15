import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import ProfileForm from "../Components/ProfileForm.js";
import SettingsModal from "../Components/SettingsModal.js";
import detectMfaEnabled from "../Controller/Auth/detectMfaEnabled.js";
import disableMFA from "../Controller/Auth/disableMFA.js";

class SettingsPage {
    async template() {
        const title1 = createElement(
            "h1",
            { class: "settings-section-title" },
            "Edit Profile"
        );
        const title2 = createElement(
            "h1",
            { class: "settings-section-title" },
            "2FA Enable/Disable"
        );
        const title3 = createElement(
            "h1",
            { class: "settings-section-title" },
            "Inactive Account"
        );
        const editProfileForm = ProfileForm();
        const mfaStatus = await detectMfaEnabled();
        const twoAuthBtn = createElement(
            "button",
            {
                class: "settings-btn",
                events: {
                    click: () => {
                        if (mfaStatus === "enabled") {
                            disableMFA();
                        } else {
                            document
                                .querySelector(".modal")
                                .classList.remove("hide");
                            document
                                .querySelector(".two-auth-package")
                                .classList.remove("hide");
                        }
                    },
                },
            },
            `2FA ${mfaStatus === "enabled" ? "Disable" : "Enable"}`
        );
        const inactiveBtn = createElement(
            "button",
            {
                class: "settings-btn",
                events: {
                    click: (event) => {
                        document
                            .querySelector(".modal")
                            .classList.remove("hide");
                        document
                            .querySelector(".inactive-account-caution")
                            .classList.remove("hide");
                        document
                            .querySelector(".settings-modal-confirm-btn")
                            .classList.remove("hide");
                    },
                },
            },
            "Inactive"
        );
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
        const modal = await SettingsModal();
        const navBar = NavBar();
        const settingsTitle = createElement(
            "h1",
            { class: "settings-title" },
            "Settings"
        );
        const sections = createElement(
            "div",
            { class: "settings-sections" },
            editProfileSection,
            twoAuthSection,
            inactivateAccountSection
        );
        const main = createElement(
            "main",
            { id: "settings-main" },
            settingsTitle,
            sections
        );
        const container = createElement("div", {}, modal, navBar, main);
        return container;
    }
}

export default SettingsPage;
