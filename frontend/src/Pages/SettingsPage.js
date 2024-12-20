import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import ProfileForm from "../Components/ProfileForm.js";
import SettingsModal from "../Components/SettingsModal.js";
import detectMfaEnabled from "../Controller/Auth/detectMfaEnabled.js";
import disableMFA from "../Controller/Auth/disableMFA.js";

class SettingsPage {
    async template(pathParam, queryParam) {
        const title1 = createElement(
            "h1",
            { class: "settings-section-title" },
            i18next.t("settings_edit_profile")
        );
        const title2 = createElement(
            "h1",
            { class: "settings-section-title" },
            i18next.t("settings_2fa")
        );
        const title3 = createElement(
            "h1",
            { class: "settings-section-title" },
            i18next.t("settings_inactive_account")
        );

        const editProfileForm = await ProfileForm();
        const mfaStatus = await detectMfaEnabled();

        const twoAuthBtn = createElement(
            "button",
            {
                class: "settings-btn two-auth-btn",
                events: {
                    click: async () => {
                        const mfaStatusAgain = await detectMfaEnabled();
                        if (mfaStatusAgain.status === "enabled") {
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
            i18next.t(
                mfaStatus.status === "enabled"
                    ? "settings_disable_2fa"
                    : "settings_enable_2fa"
            )
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
            i18next.t("settings_inactive")
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
            i18next.t("settings_title")
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
