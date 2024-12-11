import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import ProfileForm from "../Components/ProfileForm.js";

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
        const twoAuthBtn = createElement(
            "button",
            { class: "settings-btn" },
            "2FA Enable"
        );
        const inactiveBtn = createElement(
            "button",
            { class: "settings-btn" },
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
        // const modal = SettingsModal();
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
            { class: "settings-main" },
            settingsTitle,
            sections
        );
        const container = createElement("div", {}, navBar, main);
        return container;
    }
}

export default SettingsPage;


// const mfaStatus = await fetchMFAStatus();
//         console.log(mfaStatus);
//         const mfaSection = document.getElementById("mfa-section");
//         if (mfaStatus == "enabled") {
//             const mfaDisableTitle = document.createElement("h2");
//             const mfaDisableButton =
//                 document.createElement("disable-mfa-button");
//             mfaDisableTitle.textContent = "Disable MFA";
//             mfaSection.appendChild(mfaDisableTitle);
//             mfaSection.appendChild(mfaDisableButton);
//         } else {
//             const mfaEnableTitle = document.createElement("h2");
//             mfaEnableTitle.textContent = "Enable MFA";
//             const mfaQRcode = document.createElement("mfa-qr-display");
//             mfaSection.appendChild(mfaEnableTitle);
//             mfaSection.appendChild(mfaQRcode);
//             const mfaForm = createFormComponent();
//             mfaSection.appendChild(mfaForm);
//         }