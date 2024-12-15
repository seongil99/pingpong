const disableMFA = async () => {
    const url = "https://localhost/api/v1/users/accounts/mfa/"; // MFA 비활성화 API 서버 URL

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
        alert("MFA disabled!");
        window.location.reload(); // 페이지 새로고침
    } catch (error) {
        console.error("MFA disable failed:", error);
        alert("MFA disable failed!");
    }
};

export default disableMFA;
