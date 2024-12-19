const detectMfaEnabled = async () => {
    const response = await fetch("/api/v1/users/accounts/mfa/", {
        method: "GET",
        credentials: "include",
    });
    if (!response.ok) {
        return null;
    }
    return response.json();
};

export default detectMfaEnabled;