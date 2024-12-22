const enableOTP = async (otp) => {
    try {
        const response = await fetch("/api/v1/users/accounts/mfa/", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({ otp }),
        });
        if (!response.ok) {
            throw new Error(response.json());
        }
        alert(i18next.t("settings_enable_2fa"));
        document.querySelector("#otp-number-input").value = "";
        document.querySelector(".two-auth-btn").textContent = i18next.t(
            "settings_disable_2fa"
        );
        document.querySelector(".modal").classList.add("hide");
        document.querySelector(".two-auth-package").classList.add("hide");
        document
            .querySelector(".two-auth-authenticator-guide")
            .classList.add("hide");
        document
            .querySelector(".settings-modal-prev-btn")
            .classList.add("hide");
        document
            .querySelector(".settings-modal-confirm-btn")
            .classList.add("hide");
    } catch (error) {
        console.error("Error:", error);
        alert(i18next.t("settings_enable_failed_2fa"));
    }
};

export default enableOTP;
