const disableMFA = async () => {
    const url = "/api/v1/users/accounts/mfa/"; // MFA 비활성화 API 서버 URL

    try {
        const response = await fetch(url, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
        });
        if (!response.ok) {
            throw new Error(await response.json());
        }
        alert(i18next.t("settings_disable_2fa"));
        document.querySelector(".two-auth-btn").textContent = i18next.t(
            "settings_enable_2fa"
        );
    } catch (error) {
        console.error("MFA disable failed:", error);
        alert(i18next.t("settings_disable_failed_2fa"));
    }
};

export default disableMFA;
