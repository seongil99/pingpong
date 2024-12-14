const detectLoginStatus = async () => {
    const response = await fetch("/api/v1/users/accounts/verify/", {
        method: "GET",
        credentials: "include",
    });
    if (!response.ok) {
        return false;
    }
    return true;
};

export default detectLoginStatus;