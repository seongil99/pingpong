const checkMfaAuthentication = async () => {
    try {
        const response = await fetch(
            "/api/v1/users/accounts/mfa/check-login-status",
            {
                method: "GET",
                credentials: "include",
            }
        );
        if (!response.ok) {
            return false;
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
};

export default checkMfaAuthentication;
