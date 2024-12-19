const detectLoginStatus = async () => {
    try {
        const response = await fetch("/api/v1/users/accounts/verify/", {
            method: "GET",
            credentials: "include",
        });
        if (!response.ok) {
            return false;
        }
        return true;
    } catch (error) {
        console.error(error);
    }
};

export default detectLoginStatus;
