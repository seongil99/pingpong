import NavBar from "../Components/Navbar.js";
import mfaQRCode from "../Components/MfaQRCode.js";
import createFormComponent from "../Components/AuthForm.js";

const displayProfile = (userData) => {
    document.getElementById("email").querySelector("span").textContent =
        userData.email;
    const username = document.getElementById("username").querySelector("span");
    const firstName = document
        .getElementById("first-name")
        .querySelector("span");
    const lastName = document.getElementById("last-name").querySelector("span");

    if (userData.username === null || userData.username === "") {
        username.textContent = "Not provided";
    } else {
        username.textContent = userData.username;
    }
    if (userData.first_name === null || userData.first_name === "") {
        firstName.textContent = "Not provided";
    } else {
        firstName.textContent = userData.first_name;
    }
    if (userData.last_name === null || userData.last_name === "") {
        lastName.textContent = "Not provided";
    } else {
        lastName.textContent = userData.last_name;
    }
};

class SettingsPage {
    async template() {
        const mainDiv = document.createElement("div");
        mainDiv.innerHTML = `
        <div id="profile-info">
        <p id="email">Email: <span></span></p>
        <p id="username">Username: <span></span></p>
        <p id="first-name">First Name: <span></span></p>
        <p id="last-name">Lirst Name: <span></span></p>
        <button id="edit-profile">Edit Profile</button>
        </div>
        <div id="edit-profile-form" style="display: none;">
        <h2>Edit Profile</h2>
        <input type="email" id="edit-email" placeholder="Enter new email" />
        <input type="text" id="edit-first-name" placeholder="Enter new first name" />
        <input type="text" id="edit-last-name" placeholder="Enter new last name" />
        <button id="save-changes">Save Changes</button>
        <button id="cancel-edit">Cancel</button>
        </div>
        <div id="mfa-section">
        <!-- Display the MFA status here -->
        </div>
        `;

        container.appendChild(mainDiv);

        document.getElementById("app").innerHTML = ""; // Clear previous content
        document.getElementById("app").appendChild(container); // Append the profile page

        const userData = await fetchUserProfile();

        displayProfile(userData);

        const profileImage = document.createElement("img");
        profileImage.src = `${userData.avatar}`;
        profileImage.alt = "Profile Image";
        profileImage.width = 100;
        profileImage.height = 100;
        container.insertBefore(profileImage, title);

        const mfaStatus = await fetchMFAStatus();
        console.log(mfaStatus);
        const mfaSection = document.getElementById("mfa-section");
        if (mfaStatus == "enabled") {
            const mfaDisableTitle = document.createElement("h2");
            const mfaDisableButton =
                document.createElement("disable-mfa-button");
            mfaDisableTitle.textContent = "Disable MFA";
            mfaSection.appendChild(mfaDisableTitle);
            mfaSection.appendChild(mfaDisableButton);
        } else {
            const mfaEnableTitle = document.createElement("h2");
            mfaEnableTitle.textContent = "Enable MFA";
            const mfaQRcode = document.createElement("mfa-qr-display");
            mfaSection.appendChild(mfaEnableTitle);
            mfaSection.appendChild(mfaQRcode);
            const mfaForm = createFormComponent();
            mfaSection.appendChild(mfaForm);
        }

        const navBar = NavBar();
        const title = document.createElement("h2");

        const container = document.createElement("div");
        container.id = "profile-page";
        container.appendChild(navBar);
        container.appendChild(title);
        return container; // 최종 DOM 반환
    }
}

export default SettingsPage;
